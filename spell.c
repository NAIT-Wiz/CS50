// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//count the element in dictionary
unsigned int counter = 0;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int index = hash(word);
    node* curr = table[index];
    while(curr != NULL)
    {
        if (!strcasecmp(curr->word, word))
        {
            return true;
        }
        curr = curr->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen("dictionaries/large", "r");
    if (!file)
    {
        return false;
    }
    char word[LENGTH + 1];
    counter = 0;
    while (fscanf(file, "%s", word) != EOF)
    {
        node* new_node = malloc(sizeof(node));
        if (!new_node)
        {
            fclose(file);
            return false;
        }
        strcpy(new_node->word, word);
        int index = hash(word);
        new_node->next = table[index];
        table[index] = new_node;
        counter++;
    }
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    node* curr = NULL;
    node* tmp = NULL;
    for (int i = 0; i < 26; i++){
        curr = table[i];
        while(curr)
        {
            tmp = curr->next;
            free(curr);
            curr = tmp;
        }
    }
    return false;
}
