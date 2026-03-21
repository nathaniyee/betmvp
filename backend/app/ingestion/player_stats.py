from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd
import time


def normalize_name(name):
    """Normalize player name by removing suffixes and formatting"""

    name = name.lower().strip()

    suffixes = [" jr.", " jr", " sr.", " sr", " ii", " iii", " iv"]

    for suffix in suffixes:
        if name.endswith(suffix):
            name = name.replace(suffix, "")

    return name.strip()


ALL_PLAYERS = players.get_players()
PLAYER_MAP = {normalize_name(p["full_name"]): p["id"] for p in ALL_PLAYERS}


def get_player_id(player_name):
    """Return NBA player id from name using local map + fallback"""

    name = normalize_name(player_name)
    name_tokens = set(name.split())

    # Exact match
    if name in PLAYER_MAP:
        return PLAYER_MAP[name]

    # Partial match (fallback)
    best_match = None
    best_overlap = 0

    for full_name, pid in PLAYER_MAP.items():
        full_tokens = set(full_name.split())
        overlap = len(name_tokens & full_tokens)

        if overlap > best_overlap:
            best_overlap = overlap
            best_match = (full_name, pid)

    if best_match and best_overlap >= 2:
        print(f"Token match: {player_name} → {best_match[0]}")
        return best_match[1]

    raise ValueError(f"Player not found: {player_name}")


def get_last_n_games(player_name, n_games):
    """Fetch last n games for a player (n can be adjusted)"""
    player_id = get_player_id(player_name)

    for attempt in range(3):
        try:
            gamelog = playergamelog.PlayerGameLog(player_id=player_id, season="2025-26")
            df = gamelog.get_data_frames()[0]
            return df.head(n_games)

        except Exception as e:
            print(f"Retry {attempt+1} for {player_name}: {e}")
            time.sleep(1.5)

    print(f"FAILED after retries: {player_name}")
    return None


def get_stat_distribution(player_name, stat, n_games):
    """Get statistical distribution for a certain stat for a certain player over the last n games"""

    df = get_last_n_games(player_name, n_games)

    values = df[stat]

    return {"mean": values.mean(), "std": values.std(), "values": values.tolist()}
