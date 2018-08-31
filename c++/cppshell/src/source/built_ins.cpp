/**
 *  Built in commands for shell.cpp.
 *
 *  Currently contains:  cd, exit
 */

#include "helper.h"
#include "built_ins.h"

/**
 *  Change current directory.
 *
 *  @param args Tokenized vector of arguments
 *
 */

void shell_cd(std::vector<std::string> args)
{

	// Print usage if incorrect number of args
	std::string  usage = "Usage: cd directory\n";
	if ( args.size() != 2 )
		std::cerr << usage;

	// Move to new directory
	else
	{
		const char* dirname = args[1].c_str();
		int rc = 0;

		if ( (rc = chdir(dirname)) < 0 )
			custom_error("Failed to change directory", 1);
	}
}

/**
 *  Exit cppshell.
 *
 *  @param rc Return code to exit cppshell with.
 */

void shell_exit(int rc)
{
	exit(rc);
}
