#include <cs50.h>
#include <stdbool.h> // Include this for using bool data type
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
bool is_cycle(int end, int start, bool visited[]);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // Loop through the candidates to find the one with the given name
    for (int i = 0; i < candidate_count; i++)
    {
        // If the candidate is found, update ranks and preferences
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i; // Set the rank to the index of the candidate
            return true;
        }
    }
    // If the candidate is not found, return false
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // Loop through each pair of candidates
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            int winner = ranks[i];
            int loser = ranks[j];
            preferences[winner][loser]++;
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // Iterate through each pair of candidates
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            // If i is preferred over j, add it to the pairs
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
        }
    }
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = 0; j < pair_count - i - 1; j++)
        {
            int margin1 = preferences[pairs[j].winner][pairs[j].loser] - preferences[pairs[j].loser][pairs[j].winner];
            int margin2 =
                preferences[pairs[j + 1].winner][pairs[j + 1].loser] - preferences[pairs[j + 1].loser][pairs[j + 1].winner];

            // Swap if the margin of j is less than the margin of j + 1
            if (margin1 < margin2)
            {
                pair temp = pairs[j];
                pairs[j] = pairs[j + 1];
                pairs[j + 1] = temp;
            }
        }
    }
}

// Check if adding an edge from end to start will create a cycle
bool is_cycle(int start, int current, bool visited[])
{
    // If we reach the starting node again, a cycle is detected
    if (visited[current])
    {
        return true;
    }

    // Mark the current node as visited
    visited[current] = true;

    // Check all candidates
    for (int i = 0; i < candidate_count; i++)
    {
        // If there's a locked pair from the current node to another,
        // and it's not the start node, recursively check if that node leads to a cycle
        if (locked[current][i] && i != start && is_cycle(start, i, visited))
        {
            return true;
        }
    }

    // No cycle found
    return false;
}

void lock_pairs(void)
{
    // Initialize visited and stack arrays for DFS
    bool visited[candidate_count];
    bool stack[candidate_count];

    // Iterate through each pair
    for (int i = 0; i < pair_count; i++)
    {
        // Lock the current pair
        locked[pairs[i].winner][pairs[i].loser] = true;

        {
            // If adding the pair creates a cycle, unlock it
            locked[pairs[i].winner][pairs[i].loser] = false;
        }

        // Reset visited and stack arrays for the next pair
        for (int j = 0; j < candidate_count; j++)
        {
            visited[j] = false;
            stack[j] = false;
        }
    }
}
// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        bool winner = true;

        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                winner = false;
                break;
            }
        }

        if (winner)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
}
