from scipy.stats import norm
from ingestion.player_stats import get_stat_distribution


def probability_over(player_name, stat, line, n_games):
    """Calculate probability that a player exceeds a given prop line"""

    dist = get_stat_distribution(player_name, stat, n_games)

    mean = dist["mean"]
    std = dist["std"]

    prob = 1 - norm.cdf(line, loc=mean, scale=std)

    return {
        "player": player_name,
        "stat": stat,
        "line": line,
        "mean": float(mean),
        "std": float(std),
        "probability_over": float(prob),
    }
