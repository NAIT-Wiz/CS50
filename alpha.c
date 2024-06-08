#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string phrase = get_string("Enter a message: ");
    int length = strlen(phrase);
    for (int i = 0; i < length -1; i++)
    {
       //not
       if (phrase[i] > phrase[i + 1])
       {
        printf("Not In Alpha Order.\n");
        return 0;
       }
        printf("%c ", phrase[i]);
    }
    printf("\n");
}
