#include <windows.h>
#include <stdio.h>
#include <string.h>

typedef char my_bool;

typedef struct st_udf_args {
    unsigned int arg_count;
    int *arg_type;
    char **args;
    unsigned long *lengths;
    char *maybe_null;
} UDF_ARGS;

typedef struct st_udf_init {
    char maybe_null;
    unsigned int decimals;
    unsigned long max_length;
    char *ptr;
    char const_item;
} UDF_INIT;

#define STRING_RESULT 0

__declspec(dllexport) my_bool sys_exec_init(UDF_INIT *initid, UDF_ARGS *args, char *message) {
    if (args->arg_count != 1) {
        strcpy(message, "sys_exec() requires exactly one argument");
        return 1;
    }
    args->arg_type[0] = 0; // STRING_RESULT as arg type
    initid->max_length = 65535;
    initid->maybe_null = 1;
    initid->ptr = (char *)malloc(65535);
    if (initid->ptr == NULL) {
        strcpy(message, "sys_exec() failed to allocate memory");
        return 1;
    }
    return 0;
}

__declspec(dllexport) void sys_exec_deinit(UDF_INIT *initid) {
    if (initid->ptr != NULL) {
        free(initid->ptr);
    }
}

__declspec(dllexport) char *sys_exec(UDF_INIT *initid, UDF_ARGS *args, char *result,
                                       unsigned long *length, char *is_null, char *error) {
    SECURITY_ATTRIBUTES sa;
    HANDLE hReadPipe, hWritePipe;
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    char cmdline[2048];
    DWORD bytesRead;
    char buffer[4096];
    char *output = initid->ptr;
    size_t totalLen = 0;

    output[0] = '\0';

    sa.nLength = sizeof(SECURITY_ATTRIBUTES);
    sa.bInheritHandle = TRUE;
    sa.lpSecurityDescriptor = NULL;

    if (!CreatePipe(&hReadPipe, &hWritePipe, &sa, 0)) {
        strcpy(output, "ERROR: CreatePipe failed");
        *length = strlen(output);
        return output;
    }

    SetHandleInformation(hReadPipe, HANDLE_FLAG_INHERIT, 0);

    ZeroMemory(&si, sizeof(STARTUPINFOA));
    si.cb = sizeof(STARTUPINFOA);
    si.dwFlags |= STARTF_USESTDHANDLES;
    si.hStdOutput = hWritePipe;
    si.hStdError = hWritePipe;
    ZeroMemory(&pi, sizeof(PROCESS_INFORMATION));

    snprintf(cmdline, sizeof(cmdline), "cmd.exe /c %s", args->args[0]);

    if (!CreateProcessA(NULL, cmdline, NULL, NULL, TRUE, CREATE_NO_WINDOW,
                         NULL, NULL, &si, &pi)) {
        CloseHandle(hReadPipe);
        CloseHandle(hWritePipe);
        strcpy(output, "ERROR: CreateProcess failed");
        *length = strlen(output);
        return output;
    }

    CloseHandle(hWritePipe);

    while (ReadFile(hReadPipe, buffer, sizeof(buffer) - 1, &bytesRead, NULL) && bytesRead > 0) {
        buffer[bytesRead] = '\0';
        if (totalLen + bytesRead < 65534) {
            strcat(output, buffer);
            totalLen += bytesRead;
        } else {
            break;
        }
    }

    WaitForSingleObject(pi.hProcess, 5000);

    CloseHandle(hReadPipe);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    if (totalLen == 0) {
        strcpy(output, "(no output)");
        totalLen = strlen(output);
    }

    *length = totalLen;
    *is_null = 0;
    *error = 0;
    return output;
}

//compile with `x86_64-w64-mingw32-gcc -shared -o udf.dll udf.c -Wl,--add-stdcall-alias -lkernel32`
