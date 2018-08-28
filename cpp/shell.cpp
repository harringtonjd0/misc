/**
 * Basic Linux shell implementation using C++ done for learning experience. 
 * Work in progress.
 */

#include <iostream>
#include <string>
#include <vector>
#include <sys/types.h>
#include <dirent.h>

// void? parse_input()
// void? find_command()
// void? execute_command()

int main(int argc, char* argv[])
{

	while (1)
	{
		/// Take and parse user input

		// Get string from user
		std::string input;
		std::cout << "[>] ";
		getline(std::cin, input);

		// Parse string by spaces
		std::string token;
		int index = 0;
		std::vector <std::string> tokenized_input;

		while ( (index = input.find(' ')) != std::string::npos)
		{
			// Get string in between spaces
			token = input.substr(0, index);
			
			// Put token in vector
			tokenized_input.push_back(token);

			// Move next string to front
			input.erase(0, index += 1);

		} // End input parse while
		
		// Place final string in vector
		tokenized_input.push_back(input);

		// Take first token as command name
		std::string command = tokenized_input[0];
		
		/// TODO Search for command executable
		///  Move to separate function!

		// First search for built-ins
		
		// Second search for executables in PATH 


		/// TODO Execute command and return output

	} // End main while

	return 0;
}
