#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
  string strings[] = {"batteleship", "boot", "cannon", "iron", "thimble", "top hat", "busani"};

  string s = get_string("String: ");
  for (int i = 0; 1 < 7; i++)
  {
    if (strcmp(strings[i], s) == 0)
    {
    printf("Found\n");
    return 0;
    }
  }
  printf("Not found\n");
  return 1;
}
