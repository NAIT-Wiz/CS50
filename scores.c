#include <cs50.h>
#include <stdio.h>

int main (void)
{
    const int N = 4;
    int scores[N];
    for (int i = 0; i < N; i++)
    {
        scores[i] = get_int("Score: ");
    }

    printf("Average: %f\n", (scores[0] + scores[1] + scores[2] +scores[3]) / (float) N);
}
