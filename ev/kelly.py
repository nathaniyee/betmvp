def kelly_fraction(probability_win, payout_multiplier):
    """
    Calculate Kelly fraction for optimal bet size

    probability_win: probability of winning
    payout_multiplier: total payout (ex: 3 for 5x)
    """

    b = payout_multiplier - 1
    p = probability_win
    q = 1 - p

    kelly = (b * p - q) / b

    return max(kelly, 0)


def half_kelly_fraction(probability_win, payout_multiplier):
    """
    Calculate Half Kelly fraction for safer bet size
    """

    return kelly_fraction(probability_win, payout_multiplier) / 2
