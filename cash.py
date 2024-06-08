from cs50 import get_float


def calculate_change(cents):
    quarters = 0

    # Calculate quarters
    while cents >= 25:
        quarters += 1
        cents -= 25

    # Calculate dimes
    while cents >= 10:
        quarters += 1
        cents -= 10

    # Calculate nickels
    while cents >= 5:
        quarters += 1
        cents -= 5

    # Calculate pennies
    while cents >= 1:
        quarters += 1
        cents -= 1

    # Print the total number of coins
    quarters = quarters
    print(quarters)


def main():
    dollars = 0

    # Prompt the user for change owed, in cents
    while True:
        try:
            dollars = get_float("Change: ")
            if dollars is not None and dollars >= 0:
                break
        except ValueError:
            pass

    # Convert dollars to cents
    cents = int(dollars * 100)

    # Calculate the change
    calculate_change(cents)


if __name__ == "__main__":
    main()
