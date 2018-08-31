/**
 * Basic Linux shell implementation using C++ done for learning experience.
 * Could use plenty of improvement (error/signal handling, etc)
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

		/// Search for command executable

		// First, search for built-ins
		if ( (builtins.find(command)) != builtins.end() )
		{
			// Command found in builtins. Execute builtin.
			if ( command == "cd")
				shell_cd(tokenized_input);
			else
				shell_exit(0);
		}

		// Second search for executables in PATH
		else
		{
			// Get PATH variable
			std::string stdstring_path = get_env_var("PATH");

			// Tokenize path based on ':'
			std::vector<std::string> tokenized_path_vector =
				tokenize_string(stdstring_path, ":");


			// Search PATH. Probably not necessary, but good learning exercise
			DIR* dir;
			struct dirent* entry;

			int found = 0;

			// For each directory in path...
			for (size_t i = 0; i < tokenized_path_vector.size(); i++)
			{
				// Open the directory
				if ( (dir = opendir( (const char*) tokenized_path_vector[i].c_str())) != NULL )
				{
					// For each entry in the directory...
					while ( (entry = readdir(dir)) != NULL )
					{
						// Check if entry is the desired executable and execute
						if (entry->d_name == command)
						{
							found = 1;
							shell_execute(tokenized_input);
							break;
						}
					}
					closedir(dir);
				}
			}
			if (found == 0)
				std::cerr << "Command not found.\n";
		} // End command search and execution
	} // End main while

	return 0;
}
