import re
from cs50 import get_string


def validate_input(card_number):
    # Check if the input consists of digits only and is of correct length
    if re.match("^\d{13,16}$", card_number):
        return True
    else:
        return False


def get_card_type(card_number):
    if re.match("^3[47]\d{13}$", card_number):
        return "AMEX"
    elif re.match("^5[1-5]\d{14}$", card_number):
        return "MASTERCARD"
    elif re.match("^4\d{15}$", card_number):  # Adjusted regular expression for VISA
        return "VISA"
    else:
        return "INVALID"


def main():
    # Get the card number from the user
    card_number = get_string("Number: ")

    # Validate the input
    if validate_input(card_number):
        # Determine the card type
        card_type = get_card_type(card_number)
        # Print the card type followed by a newline character
        print(card_type)
    else:
        print("INVALID")


if __name__ == "__main__":
    main()
