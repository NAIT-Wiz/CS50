#include <stdio.h>
#include <cs50.h>

void print_row(int height);

int main(void)
{
    // Initialize the variable height
    int height;

    // Run the loop to get a value of height between 1 and 8, inclusive, from the user
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    // Call the function and pass height to it as a parameter
    print_row(height);
}

// Declare the function print_row
void print_row(int height)
{
    // Loop to add a new line
    for (int i = 0; i < height; i++)
    {
        // Loop to add spaces
        for (int k = height - i; k > 1; k--)
        {
            printf(" ");
        }
        // Loop to add hashes
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
