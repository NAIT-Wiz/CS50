#include <cs50.h>
#include <stdio.h>
p

int main() {
    // Define a vector of names
    std::vector<std::string> names = {"Merls", "Amari", "Nait"};

    // Prompt the user to input a name
    std::cout << "Name: ";
    std::string name;
    std::cin >> name;

    // Check if the input name is in the vector
    auto it = std::find(names.begin(), names.end(), name);
    if (it != names.end()) {
        // Name found
        std::cout << "Found" << std::endl;
    } else {
        // Name not found
        std::cout << "Not found" << std::endl;
    }

    return 0;
}

