import requests
import pandas as pd
import time

PRIZEPICKS_URL = "https://partner-api.prizepicks.com/projections"

SUPPORTED_STATS = ["Points", "Rebounds", "Assists"]

STAT_MAP = {"Points": "PTS", "Rebounds": "REB", "Assists": "AST"}


def fetch_prizepicks_props():
    """Fetch current PrizePicks projections"""
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(3):
        response = requests.get(PRIZEPICKS_URL, headers=headers)

        if response.status_code == 200:
            break

        time.sleep(1)
    else:
        raise Exception("Failed to fetch PrizePicks projections")

    if response.status_code != 200:
        raise Exception(f"PrizePicks API error: {response.status_code}")

    try:
        data = response.json()
    except Exception:
        print("PrizePicks returned non-JSON response:")
        print(response.text[:500])
        raise

    projections = data["data"]
    included = data["included"]

    # Build player lookup
    players = {}
    leagues = {}

    for item in included:

        if item["type"] == "new_player":
            players[item["id"]] = item["attributes"]["name"]

        if item["type"] == "league":
            leagues[item["id"]] = item["attributes"]["name"]

    props = []

    for proj in projections:

        attr = proj["attributes"]
        rel = proj["relationships"]

        player_rel = rel.get("new_player", {}).get("data")
        league_rel = rel.get("league", {}).get("data")

        if not player_rel or not league_rel:
            continue

        player_id = player_rel["id"]
        league_id = league_rel["id"]

        player_name = players.get(player_id)
        league_name = leagues.get(league_id)

        if attr["stat_type"] is None:
            continue

        # SKIPPING PROMO AND LIVE LINES
        if attr["is_promo"]:
            continue

        if attr["is_live"]:
            continue

        props.append(
            {
                "player": player_name,
                "stat": attr["stat_type"],
                "line": attr["line_score"],
                "league": league_name,
            }
        )

    df = pd.DataFrame(props)
    df = df[df["league"] == "NBA"]
    df = df[df["stat"].isin(SUPPORTED_STATS)]
    df["stat_column"] = df["stat"].map(STAT_MAP)

    return df
