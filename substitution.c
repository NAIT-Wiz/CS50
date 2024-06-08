#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool is_valid_key(string key);
string encrypt(string plaintext, string key);

int main(int argc, string argv[])
{
    if (argc != 2 || !is_valid_key(argv[1]))
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];
    string plaintext = get_string("plaintext: ");
    string ciphertext = encrypt(plaintext, key);

    printf("ciphertext: %s\n", ciphertext);
}

bool is_valid_key(string key)
{
    int len = strlen(key);
    if (len != 26)
    {
        return false;
    }

    int freq[26] = {0};

    for (int i = 0; i < len; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }

        int index = tolower(key[i]) - 'a';
        if (freq[index] > 0)
        {
            return false;
        }
        freq[index]++;
    }

    return true;
}

string encrypt(string plaintext, string key)
{
    int len = strlen(plaintext);

    for (int i = 0; i < len; i++)
    {
        if (isalpha(plaintext[i]))
        {
            char letter = isupper(plaintext[i]) ? 'A' : 'a';
            int key_index = tolower(plaintext[i]) - 'a';
            plaintext[i] = isupper(plaintext[i]) ? toupper(key[key_index]) : tolower(key[key_index]);
        }
    }

    return plaintext;
}
