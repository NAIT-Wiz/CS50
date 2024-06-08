#include <cs50.h>
#include <stdio.h>

typedef struct {
    string name;
    int votes;
}
candidate;

int main(void)
{
    const int num_candidates = 3;
    candidate candidates[num_candidates];

    candidates[0].name = "Busani";
    candidates[0].votes = 10;

    candidates[1].name = "Amari";
    candidates[1].votes = 15;

    candidates[2].name = "Merlo";
    candidates[2].votes = 12;

    candidates[3].name = "Memo";
    candidates[3].votes = 7;

    // todo find highets numberof votes
    int highest_votes = 0;
    for (int i = 0; i < num_candidates; i++)
    {
        if (candidates[i]. votes> highest_votes)
        {
            highest_votes = candidates[i].votes;
        }
    }
    printf("%i\n", highest_votes);

    //todo: print name of candidate with higher votes
       for (int i = 0; i < num_candidates; i++)
    {
        if (candidates[i].votes == highest_votes)
        {
            printf("%s\n", candidates[i].name);
        }
    }
}
