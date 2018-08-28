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

int shell_cd(std::vector<std::string> args)
{
	if ( args.size() < 1 )
		perror("Usage: cd directory_name");
	else if ( args.size() > 1 )
		perror("Usage: cd directory_name");
	else
	{
		const char* dirname = args[0].c_str();
		int rc = 0;
		if ( (rc = chdir(dirname)) < 0 )
			perror("Failed to change directory.\n");

		else
			return 0;
	}
	return 1;
}

