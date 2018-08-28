/**
 * Basic Linux shell implementation using C++ done for learning experience. 
 * Work in progress.
 */

#include "helper.h"
#include "built_ins.h"

int main(int argc, char* argv[])
{
	// Set of built in functions
	std::set<std::string> builtins = { "exit", "cd" };

	while (1)
	{
		/// Take and parse user input

		// Get string from user
		std::string input;
		std::cout << "[>] ";
		getline(std::cin, input);

		// Parse string by spaces
		std::vector<std::string> tokenized_input = tokenize_string(input, " ");

		// Take first token as command name and remove from vector
		std::string command = tokenized_input[0];
		tokenized_input.erase(tokenized_input.begin());
		
		/// TODO Search for command executable
		///  Move to separate function!

		// First search for built-ins
		if ( (builtins.find(command)) != builtins.end() )	
		{
			// Command found in builtins. Execute builtin.
			int rc;
			if ( command == "cd")
				rc = shell_cd(tokenized_input);
			std::cout << rc << "\n";
			//else
			//	shell_cd(tokenized_input);
		}
		
		// Second search for executables in PATH 
		else
		{	
			// Get PATH variable
			std::string stdstring_path = get_env_var("PATH");
			
			// Tokenize path based on ':'
			std::vector<std::string> tokenized_path_vector = 
				tokenize_string(stdstring_path, ":");


			// Search PATH
	/*
			DIR* dir;
			struct dirent *entry;
			
			// For each directory in path...
			for (int i = 0; i < tokenized_path_vector.size(); i++)
			{
				// Open the directory
				if ( (dir = opendir(tokenized_path_vector[i])) != NULL )
				{
					// For each entry in the directory...
					while ( (entry = readdir(dir)) != NULL )
					{
						// Check if entry is the desired executable
						if (entry == command)

					}
					closedir(dir);
				}
			}
	*/
		}
		/// TODO Execute command and return output
	} // End main while

	return 0;
}
