from ingestion.prizepicks import fetch_prizepicks_props
from ingestion.player_stats import get_last_n_games
from ev.ev_calculator import calculate_ev
from ev.kelly import kelly_fraction

import pandas as pd
from scipy.stats import norm
import time

BET_SIZE = 10
PAYOUT = 3  # assume 2-pick payout for now


def generate_bets():

    df = fetch_prizepicks_props()

    # # TEMP: limit props while debugging
    # df = df.head(30)

    results = []

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

    for _, row in df.iterrows():

        player = row["player"]
        stat = row["stat_column"]
        line = row["line"]

        try:
            stats_df = player_stats_cache[player]
            if stats_df is None:
                continue

            # reuse the cached stats to compute probability
            values = stats_df[stat]

            mean = values.mean()
            std = values.std()

            if std == 0:
                continue

            prob = 1 - norm.cdf(line, loc=mean, scale=std)

            ev = calculate_ev(
                probability_win=prob, bet_amount=BET_SIZE, payout_multiplier=PAYOUT
            )

            kelly = kelly_fraction(probability_win=prob, payout_multiplier=PAYOUT)

            results.append(
                {
                    "player": player,
                    "stat": stat,
                    "line": line,
                    "probability": prob,
                    "ev": ev,
                    "kelly_fraction": kelly,
                }
            )

        except Exception as e:
            print(f"Skipping {player} {stat}: {e}")

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("ev", ascending=False)
    return results_df


if __name__ == "__main__":
    df = generate_bets()
    print(df.head(20))
