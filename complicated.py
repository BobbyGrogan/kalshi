import numpy as np
import math

# Function to get user input
def get_input(prompt, cast_type=float):
    while True:
        try:
            return cast_type(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to simulate a single GBM price path without drift
def simulate_gbm_path(start_price, daily_volatility, intraday_volatility, increments, time_fraction):
    prices = [start_price]
    for i in range(increments):
        local_volatility = daily_volatility * intraday_volatility[i % len(intraday_volatility)]
        random_shock = np.random.normal(0, 1) * math.sqrt(time_fraction)
        change = - (0.5 * local_volatility**2 * time_fraction) + (local_volatility * random_shock)
        prices.append(prices[-1] * math.exp(change))
    return prices

# Main program
print("Welcome to the Fair Odds Calculator!")
print("This program uses Geometric Brownian Motion (no drift) to calculate fair odds for events.")

# Get initial setup inputs
daily_volatility_percent = get_input("Enter the daily volatility percentage: ", float)
time_increment_minutes = get_input("Enter the time increment in minutes (e.g., 5): ", int)
total_minutes = get_input("Enter the total simulation time in minutes (e.g., 120): ", int)
simulations = get_input("Enter the number of simulations to run: ", int)

# Convert inputs
daily_volatility = daily_volatility_percent / 100
increments_per_day = 1440 / time_increment_minutes
time_increment_fraction = time_increment_minutes / 1440

# Allow for optional intraday volatility scaling
intraday_volatility = np.ones(int(increments_per_day))  # Default: constant volatility
use_intraday = input("Do you want to provide intraday volatility data (y/n)? ").lower()
if use_intraday == 'y':
    print("Enter intraday volatility percentages for each time increment (separated by spaces):")
    intraday_volatility = [float(v) / 100 for v in input().split()]
    if len(intraday_volatility) != increments_per_day:
        print("Error: Intraday volatility data must have exactly", int(increments_per_day), "entries.")
        exit()

# Repeated fair odds calculation
while True:
    # Get bet-specific inputs
    start_price = get_input("\nEnter the starting price: ", float)
    goal_price = get_input("Enter the goal price: ", float)

    # Run simulations
    hits = 0
    for _ in range(simulations):
        path = simulate_gbm_path(start_price, daily_volatility, intraday_volatility, total_minutes // time_increment_minutes, time_increment_fraction)
        if path[-1] > goal_price:
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
    print(f"Fair odds in favor of goal price: {fair_odds_in_favor:.2f}:1")
    print(f"Fair odds against the goal price: {fair_odds_against:.2f}:1")

    # Ask to run again or exit
    run_again = input("\nDo you want to calculate fair odds for another event? (y/n): ").lower()
    if run_again != 'y':
        print("Thank you for using the Fair Odds Calculator! Goodbye!")
        break
