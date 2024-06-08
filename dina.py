import csv
import sys

def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python script.py database.csv sequence.txt")
        sys.exit(1)

    # Get file names from command-line arguments
    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    # Read database file into a variable
    with open(database_file, newline='') as f:
        database = list(csv.reader(f))

    # Read DNA sequence file into a variable
    with open(sequence_file, 'r') as f:
        sequence = f.read()

    # TODO: Find longest match of each STR in DNA sequence

    # TODO: Check database for matching profiles

if __name__ == "__main__":
    main()

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()












import csv
import sys

def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python script.py database.csv sequence.txt")
        sys.exit(1)

    # Get file names from command-line arguments
    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    # Read database file into a variable
    with open(database_file, newline='') as f:
        database = list(csv.reader(f))

    # Read DNA sequence file into a variable
    with open(sequence_file, 'r') as f:
        sequence = f.read()

    # Extract the STRs and corresponding counts from the database
    headers = database[0][1:]
    profiles = {row[0]: [int(count) for count in row[1:]] for row in database[1:]}

    # Calculate the counts of each STR in the sequence
    sequence_str_counts = {header: count_str(sequence, header) for header in headers}

    # Check for matching profiles
    for name, profile in profiles.items():
        if profile == [sequence_str_counts[header] for header in headers]:
            print(name)
            return

    print("No match")

def count_str(sequence, subsequence):
    """Counts the occurrences of subsequence in sequence."""
    count = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Iterate through the sequence and count occurrences of subsequence
    i = 0
    while i < sequence_length:
        # Check if the subsequence starts at the current position
        if sequence[i:i+subsequence_length] == subsequence:
            count += 1
            # Move to the next potential match in sequence
            i += subsequence_length
        else:
            i += 1

    return count

if __name__ == "__main__":
    main()
