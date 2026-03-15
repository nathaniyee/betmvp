from ingestion.prizepicks import fetch_prizepicks_props
from ingestion.player_stats import get_last_n_games
from ev.ev_calculator import calculate_single_ev
from ev.kelly import kelly_fraction

import pandas as pd
from scipy.stats import norm
import time

# BET_SIZE = 10

# approximate single-pick payouts for ranking
STANDARD_PAYOUT = 2.0
GOBLIN_PAYOUT = 1.6
DEMON_PAYOUT = 3.5

# assume market probability for standard squares
MARKET_PROB = 0.5

def score_standard_props(df, player_stats_cache):
    """Score standard props and choose the best side (over/under)"""

    results = []

    for _, row  in df.iterrows():

        player = row["player"]
        stat = row["stat_column"]
        line = row["line"]

        stats_df = player_stats_cache.get(player)
        if stats_df is None:
            continue

        try:

            values = stats_df[stat]

            mean = values.mean()
            std = values.std()

            if pd.isna(std) or std == 0:
                continue

            prob_over = 1 - norm.cdf(line, loc=mean, scale=std)
            prob_under = norm.cdf(line, loc=mean, scale=std)

            if prob_over >= prob_under:
                bet_side = "OVER"
                probability = prob_over
            else:
                bet_side = "UNDER"
                probability = prob_under

            edge = probability - MARKET_PROB
            ev = calculate_single_ev(probability, STANDARD_PAYOUT)
            kelly = kelly_fraction(probability, STANDARD_PAYOUT)

            results.append({
                "Player": player,
                "Stat": stat,
                "Line": line,
                "Bet": bet_side,
                "Probability": probability,
                "Edge": edge,
                "EV": ev,
                "Kelly Bet": kelly
            })

        except Exception:
            continue

    return pd.DataFrame(results)
        
def score_one_sided_props(df, player_stats_cache, payout):
    """Score goblins or demons where only one side matters."""

    results = []

    for _, row in df.iterrows():

        player = row["player"]
        stat = row["stat_column"]
        line = row["line"]

        stats_df = player_stats_cache.get(player)
        if stats_df is None:
            continue

        try:

            values = stats_df[stat]

            mean = values.mean()
            std = values.std()

            if pd.isna(std) or std == 0:
                continue

            prob_over = 1 - norm.cdf(line, loc=mean, scale=std)

            probability = prob_over

            edge = probability - MARKET_PROB
            ev = calculate_single_ev(probability, payout)
            kelly = kelly_fraction(probability, payout)

            results.append({
                "Player": player,
                "Stat": stat,
                "Line": line,
                "Bet": "OVER",
                "Probability": probability,
                "Edge": edge,
                "EV": ev,
                "Kelly Bet": kelly
            })

        except Exception:
            continue

    return pd.DataFrame(results)

def format_output(df):

    if df.empty:
        return df

    df = df.copy()

    df["Probability"] = (df["Probability"] * 100).round(0).astype(int).astype(str) + "%"
    df["Edge"] = (df["Edge"] * 100).round(0).astype(int).astype(str) + "%"
    df["EV"] = df["EV"].round(2)
    df["Kelly Bet"] = (df["Kelly Bet"] * 100).round(0).astype(int).astype(str) + "%"

    return df


def generate_bets():

    df = fetch_prizepicks_props()

    standard_df = df[df["odds_type"] == "standard"]
    goblin_df = df[df["odds_type"] == "goblin"]
    demon_df = df[df["odds_type"] == "demon"]

    # cache to avoid repeated NBA API calls for the same player
    player_stats_cache = {}

    unique_players = df["player"].unique()

    for p in unique_players:
        try:
            if p not in player_stats_cache:
                player_stats_cache[p] = get_last_n_games(p, 20)
                time.sleep(0.6)  # prevent NBA API rate limiting
        except Exception as e:
            print(f"Failed to fetch stats for {p}: {e}")

    # Score props
    standard_scores = score_standard_props(standard_df, player_stats_cache)

    goblin_scores = score_one_sided_props(goblin_df, player_stats_cache, GOBLIN_PAYOUT)
    demon_scores = score_one_sided_props(demon_df, player_stats_cache, DEMON_PAYOUT)

    # Split overs and unders
    top_overs = standard_scores[standard_scores["Bet"] == "OVER"]
    top_unders = standard_scores[standard_scores["Bet"] == "UNDER"]

    # Rank
    top_overs = top_overs.sort_values("EV", ascending=False).head(10)
    top_unders = top_unders.sort_values("EV", ascending=False).head(10)

    top_goblins = goblin_scores.sort_values("EV", ascending=False).head(10)
    top_demons = demon_scores.sort_values("EV", ascending=False).head(10)

    # Format
    top_overs = format_output(top_overs)
    top_unders = format_output(top_unders)
    top_goblins = format_output(top_goblins)
    top_demons = format_output(top_demons)

    return top_overs, top_unders, top_goblins, top_demons

if __name__ == "__main__":

    overs, unders, goblins, demons = generate_bets()

    print("\nTOP 10 OVERS\n")
    print(overs[["Player", "Stat", "Line", "Probability", "Edge", "EV", "Kelly Bet"]])

    print("\nTOP 10 UNDERS\n")
    print(unders[["Player", "Stat", "Line", "Probability", "Edge", "EV", "Kelly Bet"]])

    print("\nTOP 10 GOBLINS\n")
    print(goblins[["Player", "Stat", "Line", "Probability", "Edge", "EV", "Kelly Bet"]])

    print("\nTOP 10 DEMONS\n")
    print(demons[["Player", "Stat", "Line", "Probability", "Edge", "EV", "Kelly Bet"]])
