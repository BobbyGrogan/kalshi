import random
import math

# Parameters
start_price = 92324
goal_price = 92750
daily_volatility_percent = 2.26  # Daily volatility as a percentage
time_increment_minutes = 5  # 5-minute increments
total_minutes = 120  # Total simulation time (e.g., 24 periods = 2 hours)
simulations = 10000
hits = 0

# Convert daily volatility percent to decimal
daily_volatility = daily_volatility_percent / 100

# Scale volatility to 5-minute intervals
increment_volatility = daily_volatility * math.sqrt(time_increment_minutes / 1440)

# Calculate change range per 5-minute interval
change_range = increment_volatility * start_price

# Simulate price movements
for _ in range(simulations):
    price = start_price
    for _ in range(total_minutes // time_increment_minutes):  # Number of 5-minute periods
        price += random.uniform(-change_range, change_range)
    if price > goal_price:
        hits += 1

# Calculate probability
probability = hits / simulations
fair_odds = 1 / probability

# Offered odds - bet 1 to win x.xx
offered_odds = 1.85

# Output
print(f"Probability of price > {goal_price}: {probability:.4f}")
print(f"Fair odds: {fair_odds:.2f}:1 vs Offered odds: {offered_odds:.2f}:1")

# Determine if the bet is undervalued
if fair_odds > offered_odds:
    print("The bet is overvalued. (Not a good value)")
else:
    print("The bet is undervalued. (Good value to bet)")
