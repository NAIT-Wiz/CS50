from cs50 import get_float

def calculate_change(cents):
    quarters = 0
    dimes = 0
    nickels = 0
    pennies = 0

    # Calculate quarters
    while cents >= 25:
        quarters += 1
        cents -= 25

    # Calculate dimes
    while cents >= 10:
        dimes += 1
        cents -= 10

    # Calculate nickels
    while cents >= 5:
        nickels += 1
        cents -= 5

    # Calculate pennies
    while cents >= 1:
        pennies += 1
        cents -= 1

    # Print the total number of coins
    total_coins = quarters + dimes + nickels + pennies
    print(total_coins)

def main():
    dollars = 0

    # Prompt the user for change owed in dollars
    while True:
        dollars = get_float("Change owed (in dollars): ")
        if dollars is not None and dollars >= 0:
            break

    # Convert dollars to cents
    cents = round(dollars * 100)

    # Calculate the change
    calculate_change(cents)

if __name__ == "__main__":
    main()
