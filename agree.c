#include <cs50.h>
#include <stdio.h>

int main(void)
{
    char c = get_char("do you agree? ");

    if (c == 'y'|| c == 'Y')
    {
        printf("Agreed.\n");
    }
    else if (c =='n'|| c == 'N')
    {
        printf(" agreed.\n");
    }

