#include <cs50.h>
#include <stdio.h>

void calculate_change(int cents);

int main(void)
{
    int cents;

    // Prompt the user for change owed, in cents
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    // Calculate the change
    calculate_change(cents);
}

void calculate_change(int cents)
{
    int quarters = 0;

    // Calculate quarters
    while (cents >= 25)
    {
        quarters++;
        cents -= 25;
    }

    // Calculate dimes
    while (cents >= 10)
    {
        quarters++;
        cents -= 10;
    }

    // Calculate nickels
    while (cents >= 5)
    {
        quarters++;
        cents -= 5;
    }

    // Calculate pennies
    while (cents >= 1)
    {
        quarters++;
        cents -= 1;
    }

    // Print the total number of coins
    printf("%i\n", quarters);
}
