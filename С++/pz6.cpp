#include <iostream>
#include <windows.h>
#include <direct.h>
#include <tlhelp32.h>

int main() {
    // Системное время
    SYSTEMTIME t;
    GetLocalTime(&t);
    std::cout << "Время: " << t.wHour << ":" << t.wMinute << ":" << t.wSecond << "\n";
    
    // Рабочий каталог
    char dir[500];
    _getcwd(dir, 500);
    std::cout << "Каталог: " << dir << "\n";
    
    // Тип файловой системы
    char fs[100];
    GetVolumeInformation("C:\\", 0, 0, 0, 0, 0, fs, 100);
    std::cout << "Файловая система: " << fs << "\n\n";
    
    // Все процессы
    std::cout << "Все процессы:\n";
    HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(pe);
    
    if (Process32First(snap, &pe)) {
        do {
            std::cout << pe.szExeFile << "\n";
        } while (Process32Next(snap, &pe));
    }
    
    CloseHandle(snap);
    
    std::cout << "\nНажмите Enter...";
    std::cin.get();
    return 0;
}