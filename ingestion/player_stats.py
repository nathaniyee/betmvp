from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd

ALL_PLAYERS = players.get_players()

PLAYER_MAP = {
    p["full_name"].lower(): p["id"]
    for p in ALL_PLAYERS
}

def get_player_id(player_name):
    """Return NBA player id from name using local map + fallback"""

    name = player_name.lower()

    # Exact match
    if name in PLAYER_MAP:
        return PLAYER_MAP[name]
    
    #Partial match (fallback)
    for full_name, pid in PLAYER_MAP.items():
        if name in full_name or full_name in name:
            print(f"Fallback match: {player_name} → {full_name}")
            return pid

    raise ValueError(f"Player not found: {player_name}")


def get_last_n_games(player_name, n_games):
    """Fetch last n games for a player (n can be adjusted)"""
    player_id = get_player_id(player_name)

    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season="2025-26")

    df = gamelog.get_data_frames()[0]

    return df.head(n_games)


def get_stat_distribution(player_name, stat, n_games):
    """Get statistical distribution for a certain stat for a certain player over the last n games"""

    df = get_last_n_games(player_name, n_games)

    values = df[stat]

    return {"mean": values.mean(), "std": values.std(), "values": values.tolist()}
