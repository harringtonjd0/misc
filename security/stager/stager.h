#ifndef MAIN_LIBS_H
#define MAIN_LIBS_H
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <winsock2.h>
#include <wS2tcpip.h>
#include <stdlib.h>
#include <stdio.h>

#pragma comment (lib, "Ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "advApi32.lib")

#define DEFAULT_BUFLEN 1024
#endif MAIN_LIBS_H

// prep functions
#ifndef PREP
#define PREP
#include "prep.h"
#endif PREP
