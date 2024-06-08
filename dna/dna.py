import csv
import sys
from sys import argv
import re


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python script.py database.csv sequence.txt")
        sys.exit(1)

    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    # Read database file into a variable
    with open(database_file, newline='') as f:
        database = list(csv.reader(f))

    # Read DNA sequence file into a variable
    with open(sequence_file, 'r') as f:
        sequence = f.read()

    # Find longest match of each STR in DNA sequence
    headers = database[0][1:]
    profiles = {row[0]: [int(count) for count in row[1:]] for row in database[1:]}
    sequence_str_counts = {header: longest_match(sequence, header) for header in headers}

    # Define the tolerance level (adjust this value as needed)
    tolerance = 0.01  # 1%

    # Check database for matching profiles
    for name, profile in profiles.items():
        match = True
        for header, count in zip(headers, profile):
            if abs(sequence_str_counts[header] - count) / count > tolerance:
                match = False
                break
        if match:
            print(name)
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    i = 0
    while i < sequence_length:
        count = 0
        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        while sequence[i:i+subsequence_length] == subsequence:
            count += 1
            i += subsequence_length

        # Update most consecutive matches found
        longest_run = max(longest_run, count)
        i += 1

    return longest_run


if __name__ == "__main__":
    main()
