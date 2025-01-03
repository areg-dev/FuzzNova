#include <iostream>
#include <cstdio>

#define BUFFER_SIZE 10

int main() {
    char buffer[BUFFER_SIZE];
    std::cout << "Enter a string:" << std::endl;
    // This is UNSAFE and can lead to buffer overflow
    scanf("%s", buffer);
    std::cout << "You entered: " << buffer << std::endl;
    return 0;
}
