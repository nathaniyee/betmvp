from backend.app.models.probability_model import probability_over

result_curry = probability_over("Stephen Curry", stat="PTS", line=29.5, n_games=20)

result_shai = probability_over(
    "Shai Gilgeous-Alexander", stat="PTS", line=33, n_games=20
)

print(result_shai)
