from backend.app.ingestion.player_stats import get_last_n_games

df_curry = get_last_n_games("Stephen Curry", 20)
df_durant = get_last_n_games("Kevin Durant", 5)

print(df_curry.columns)
print(df_curry[["GAME_DATE", "PTS", "REB", "AST"]])
print(df_durant[["GAME_DATE", "PTS", "REB", "AST"]])
