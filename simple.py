import random
import math

# Function to get user input
def get_input(prompt, cast_type=float):
    while True:
        try:
            return cast_type(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Get user inputs
start_price = get_input("Enter the starting price: ", float)
goal_price = get_input("Enter the goal price: ", float)
daily_volatility_percent = get_input("Enter the daily volatility percentage: ", float)
time_increment_minutes = get_input("Enter the time increment in minutes (e.g., 5): ", int)
total_minutes = get_input("Enter the total simulation time in minutes (e.g., 120): ", int)
simulations = get_input("Enter the number of simulations to run: ", int)
offered_odds = get_input("Enter the offered odds (e.g., 1.85): ", float)
bet_type = get_input("Enter 1 to bet in favor of the goal price, or 0 to bet against it: ", int)

# Convert daily volatility percent to decimal
daily_volatility = daily_volatility_percent / 100

# Scale volatility to match the time increment
increment_volatility = daily_volatility * math.sqrt(time_increment_minutes / 1440)

# Calculate change range per time increment
change_range = increment_volatility * start_price

# Simulate price movements
hits = 0
for _ in range(simulations):
    price = start_price
    for _ in range(total_minutes // time_increment_minutes):  # Number of increments
        price += random.uniform(-change_range, change_range)
    if price > goal_price:
        hits += 1

# Calculate probabilities
probability_in_favor = hits / simulations
probability_against = 1 - probability_in_favor

# Determine fair odds
fair_odds_in_favor = float('inf') if probability_in_favor == 0 else 1 / probability_in_favor
fair_odds_against = float('inf') if probability_against == 0 else 1 / probability_against

# Output results
print(f"\nResults:")
print(f"Probability of price > {goal_price}: {probability_in_favor:.4f}")
print(f"Probability of price <= {goal_price}: {probability_against:.4f}")

if bet_type == 1:
    print(f"Fair odds in favor of goal price: {fair_odds_in_favor:.2f}:1 vs Offered odds: {offered_odds:.2f}:1")
    if probability_in_favor == 0:
        print("The bet is overvalued. (The probability of success is effectively zero)")
    elif fair_odds_in_favor > offered_odds:
        print("The bet is overvalued. (Not a good value)")
    else:
        print("The bet is undervalued. (Good value to bet)")
elif bet_type == 0:
    print(f"Fair odds against the goal price: {fair_odds_against:.2f}:1 vs Offered odds: {offered_odds:.2f}:1")
    if probability_against == 0:
        print("The bet is overvalued. (The probability of success is effectively zero)")
    elif fair_odds_against > offered_odds:
        print("The bet is overvalued. (Not a good value)")
    else:
        print("The bet is undervalued. (Good value to bet)")
else:
    print("Invalid bet type. Please enter 1 (in favor) or 0 (against).")
