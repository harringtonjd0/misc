#include <iostream>
#include <stdio.h>
#include <error.h>
#include <sys/types.h>
#include <dirent.h>

int main()
{
	const char* dirname = "/usr/bin";
	DIR* dir;
	struct dirent *entry;

	if ( (dir = opendir(dirname)) != NULL )
	{
		while ( (entry = readdir(dir)) != NULL )
			printf("%s\n", entry->d_name);
		closedir(dir);
	}
	else
	{
		perror("Couldn't open directory.\n");
		return EXIT_FAILURE;
	}

	return 0;
}
