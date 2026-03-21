def calculate_ev(probability_win, bet_amount, payout_multiplier):
    """
    Calculate expected value of a bet

    probability_win: model probability of winning
    bet_amount: amount wagered
    payout_multiplier: total payout (ex. 3 for 5x)
    """

    profit_if_win = bet_amount * (payout_multiplier - 1)

    probability_loss = 1 - probability_win

    ev = (probability_win * profit_if_win) - (probability_loss * bet_amount)

    return ev


def calculate_single_ev(probability_win, payout_multiplier):
    """
    Calculate expected value of a bet

    probability_win: model probability of winning
    payout_multiplier: total payout
    """

    return probability_win * payout_multiplier - (1 - probability_win)
