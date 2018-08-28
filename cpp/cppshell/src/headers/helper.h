/** 
 * 	Header for helper.c.
 * 	Contains all includes used by cppshell.
 */

#include <iostream>
#include <stdio.h>
#include <cstdlib>
#include <string>
#include <vector>
#include <sys/types.h>
#include <dirent.h>
#include <set>

std::string get_env_var(std::string const& key);
std::vector<std::string> tokenize_string(std::string input, std::string delim);

