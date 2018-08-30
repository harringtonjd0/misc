/**
 * 	Helper functions for cppshell
 */

#include "helper.h"
#include "built_ins.h"

/**
 * Handle errors and exit program.
 *
 * @param errmsg The string to print in the error message.
 * @param rc The return code to exit the program with.
 */

void custom_error(std::string errmsg, int rc)
{
	// Output custom error message
	const char* strerror_msg = std::strerror(errno);
	std::cerr << "[!] ERROR: " << errmsg << "\n\t==> [Errno " << errno << "] "
	      	<< strerror_msg << "\n";

	// Exit program with given error code
	exit(rc);

}

/**
 * Get environment variable by name
 *
 * @param key The name of the environment variable to access
 * @return String containing environment variable contents
 *
 * Taken from https://stackoverflow.com/questions/631664/accessing-environment-variables-in-c
 */

std::string get_env_var(std::string const& key)
{
	char* val = std::getenv( key.c_str() );
	return val == NULL ? std::string("") : std::string(val);
}

/**
 * Split string into tokenized vector based on delimiter
 *
 * @param input The string to tokenize
 * @param delim The delimiter to use
 * @return Vector containing tokenized string
 */

std::vector<std::string> tokenize_string(std::string input, std::string delim)
{
	// Parse string by spaces
	std::string token;
	size_t index = 0;
	std::vector <std::string> tokenized_input;

	while ( (index = input.find(delim)) != std::string::npos)
	{
		// Get string in between spaces
		token = input.substr(0, index);

		// Put token in vector
		tokenized_input.push_back(token);

		// Move next string to front
		input.erase(0, index += delim.length());

	} // End input parse while

	// Place final string in vector
	tokenized_input.push_back(input);

	// Return vector of tokenized strings
	return tokenized_input;
}

/**
 *	Execute command with fork() and execvp()
 *
 *	@param command The command to execute
 *	@param args The tokenized vector of arguments to pass to the executable
 *
 */

void shell_execute(std::string command, std::vector<std::string> args)
{
	const char* argv[] = { "ls", "-la", NULL };

	pid_t child_pid;
	int child_status;

	if ( (child_pid= fork()) < 0)
	{
		std::cout << "Failed to fork.\n";
		exit(1);
	}
	else if (child_pid== 0)
	{
		if ( execvp( (const char*) argv[0],  (char* const*) argv) < 0 )
		{
			std::cout << "Failed to exec.\n";
			exit(2);
		}
	}
	else
	{
		while ( wait(&child_status) != child_pid)
			;
	}

}
