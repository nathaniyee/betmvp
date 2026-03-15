# BetMVP Design Document

## Project Overview
The goal of this project is to build a dashboard that analyzes PrizePicks player props and identifies positive expected value betting opportunities.

The system will:
1. Pull PrizePicks player prop lines
2. Estimate true probability of prop hitting
3. Calculate expected value
4. Recommend bet size using Kelly Criterion

Example Output:
| Player  | Prop       | Line | Model Prob | Edge | Kelly Bet |
|--------|------------|------|------------|------|-----------|
| S. Curry | Points +   | 29.5 | 61%        | +11% | 3.8%      |
| N. Jokic | Rebounds + | 11.5 | 58%        | +8%  | 2.9%      |


## MVP Scope (v1)
We do NOT need a perfect model yet. The v1 goals are as follows:

Core Features:
Pull PrizePicks prop lines (daily refresh)
Pull historical player stats
Estimate probability using simple model
Calculate expected value
Calculate Kelly bet size
Display results in a dashboard (best bets at top)


## System Architecture
PrizePicks API -> Data Collector -> Player Stats API -> Probability Model -> EV + Kelly Calculation -> Frontend Dashboard

## 4. Tech Stack


## 5. Project Folder Structure


## 6. Data Sources
The BetMVP system relies on two primary data sources:
- PrizePicks Projection Data: publicly available PrizePicks API that provides the available betting lines
- NBA Historical Player Statistics: publicly available API Client for NBA.com that is used to create probability model to estimate probability of prop outcome occurring 


## 7. Probability Model


## EV Calculation
PrizePicks payouts:
- 2 picks → 3x
- 3 picks → 5x
- 4 picks → 10x

Example:
- Bet: $100
- 2 picks Payout: $300
- Profit: $200

EV Formula: *EV = ((P(win) * profit) - P(loss) * bet)*

Break-even probability is ⅓ = 33.33%. Suppose the model predicts P(win) = 40%. This means the edge is 40% - 33.33% = +6.7%. Thus the model thinks the bet is 6.7% better than fair odds. 



## Kelly Criterion
Kelly Criterion Formula: *f = (bp - q) / b*
- b = odds
- p = probability win
- q = probability loss 

Example: 
- p = 0.40
- b = 2
- f = (2 * 0.40 - 0.60) / 2 = 0.1
- Bet **10%** of bankroll



## 10. Dashboard Design