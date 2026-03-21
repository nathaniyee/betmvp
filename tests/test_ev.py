from ev.ev_calculator import calculate_ev
from ev.kelly import kelly_fraction

prob = 0.40
bet = 100
payout = 3

ev = calculate_ev(prob, bet, payout)

kelly = kelly_fraction(prob, payout)

print("EV:", ev)
print("Kelly fraction:", kelly, "meaning bet", int(kelly * 100), "% of bankroll.")
