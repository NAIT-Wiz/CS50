def print_row(height):
    for i in range(height):
        for k in range(height - i - 1):
            print(" ", end="")
        for j in range(i + 1):
            print("#", end="")
        print()


def main():
    # Run the loop to get a value of height between 1 and 8, inclusive, from the user
    while True:
        try:
            height_input = input("Height: ")
            height = int(height_input)
            if height >= 1 and height <= 8:
                break
            else:
                print("Height must be between 1 and 8, inclusive.")
        except ValueError:
            print("Height must be a numeric value.")

    # Call the function and pass height to it as a parameter
    print_row(height)


if __name__ == "__main__":
    main()
