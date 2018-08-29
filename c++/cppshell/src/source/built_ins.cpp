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
	const char*  usage = "Usage: cd directory";
	if ( (args.size() < 1) or (args.size() > 1 ) )
		fprintf(stderr, "%s\n", usage);
	
	// Move to new directory
	else
	{
		const char* dirname = args[0].c_str();
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


