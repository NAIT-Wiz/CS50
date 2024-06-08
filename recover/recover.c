#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");

    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];

    // Counter for JPEG files found
    int jpeg_count = 0;

    // Output file pointer
    FILE *output = NULL;

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        // Check if the current block is the start of a new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If we already found a JPEG, close the previous one
            if (output != NULL)
            {
                fclose(output);
            }

            // Create a new JPEG file
            char filename[8];
            sprintf(filename, "%03i.jpg", jpeg_count);
            output = fopen(filename, "w");
            if (output == NULL)
            {
                fclose(card);
                fprintf(stderr, "Could not create %s\n", filename);
                return 2;
            }

            jpeg_count++;
        }

        // If we have found a JPEG, write the block to the file
        if (output != NULL)
        {
            fwrite(buffer, 1, 512, output);
        }
    }

    // Close files
    fclose(card);
    if (output != NULL)
    {
        fclose(output);
    }

    return 0;
}
