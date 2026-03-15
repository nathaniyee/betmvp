from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import pandas as pd


def get_player_id(player_name):
    """Return NBA player ID from name"""

    player_dict = players.find_players_by_full_name(player_name)

    if not player_dict:
        raise ValueError("Player not found!")

    return player_dict[0]["id"]


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
