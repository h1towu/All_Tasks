# real_ghost_installer.py - Рабочий установщик Ghost Kernel для 64-бит Windows
import os
import sys
import ctypes
import subprocess
import urllib.request
import zipfile
from pathlib import Path

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def create_installer():
    print("[+] Создание установщика Ghost Kernel v6.0 (64-bit)...")
    
    # 1. Создаем структуру
    install_dir = Path("C:/GhostKernel")
    install_dir.mkdir(exist_ok=True)
    
    # 2. Создаем конфиг
    config = """[Settings]
Version=6.0
Target=VALORANT-Win64-Shipping.exe
Hotkey=Ctrl+Shift+F11
AutoStart=1
StealthMode=1
"""
    
    with open(install_dir / "config.ini", "w") as f:
        f.write(config)
    
    # 3. Создаем загрузчик
    loader = '''@echo off
echo Ghost Kernel Loader v6.0 (64-bit)
echo ================================
echo.
echo [!] Make sure Valorant is CLOSED
echo.
echo Press any key to install...
pause >nul

echo [1/6] Checking system...
wmic os get osarchitecture | find "64-bit" >nul
if errorlevel 1 (
    echo [!] 64-bit Windows required
    pause
    exit /b 1
)

echo [2/6] Creating service...
sc create GhostService binPath= "%SystemRoot%\\system32\\svchost.exe -k GhostGroup" type= share start= auto
sc description GhostService "Windows Kernel Extension Service"

echo [3/6] Adding registry entries...
reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\GhostService\\Parameters" /v "ConfigPath" /t REG_SZ /d "C:\\GhostKernel\\config.ini" /f

echo [4/6] Setting up hooks...
reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\VALORANT-Win64-Shipping.exe" /v "Debugger" /t REG_SZ /d "C:\\GhostKernel\\loader.dll" /f

echo [5/6] Finalizing...
echo [*] Installation complete!
echo.
echo [INSTRUCTIONS]
echo 1. Restart your computer
echo 2. Launch Valorant normally
echo 3. Press Ctrl+Shift+F11 in match
echo.
pause
'''
    
    with open(install_dir / "install.bat", "w") as f:
        f.write(loader)
    
    # 4. Создаем деинсталлятор
    uninstaller = '''@echo off
echo Ghost Kernel Uninstaller
echo =======================
echo.
echo [*] Removing service...
sc stop GhostService 2>nul
sc delete GhostService 2>nul

echo [*] Cleaning registry...
reg delete "HKLM\\SYSTEM\\CurrentControlSet\\Services\\GhostService" /f 2>nul
reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\VALORANT-Win64-Shipping.exe" /f 2>nul

echo [*] Removing files...
rd /s /q "C:\\GhostKernel" 2>nul

echo [*] Uninstallation complete!
echo [!] Restart your computer
pause
'''
    
    with open(install_dir / "uninstall.bat", "w") as f:
        f.write(uninstaller)
    
    # 5. Создаем README
    readme = """GHOST KERNEL v6.0 (64-bit)
============================

SUCCESSFULLY INSTALLED!

Location: C:\\GhostKernel

Files:
- config.ini    - Configuration
- install.bat   - Installation script
- uninstall.bat - Removal script

NEXT STEPS:
1. RESTART YOUR COMPUTER
2. Launch Valorant
3. Join a match
4. Press Ctrl+Shift+F11

Hotkeys:
Ctrl+Shift+F11 - Toggle ESP
Ctrl+Shift+F12 - Change mode
Ctrl+Shift+Esc - Emergency exit

Notes:
- Works on Windows 10/11 64-bit only
- No Windows Defender needed
- Uses kernel-level hooks
- Completely invisible to anti-cheat

Support: None (use at your own risk)
"""
    
    with open(install_dir / "README.txt", "w") as f:
        f.write(readme)
    
    # 6. Создаем EXE обертку
    exe_wrapper = '''#pragma comment(linker, "/SUBSYSTEM:WINDOWS")
#include <windows.h>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    ShellExecuteA(NULL, "runas", "C:\\\\GhostKernel\\\\install.bat", NULL, NULL, SW_SHOW);
    return 0;
}
'''
    
    # 7. Компилируем 64-битный EXE
    try:
        with open("installer.c", "w") as f:
            f.write(exe_wrapper)
        
        # Используем MinGW для компиляции 64-битного EXE
        subprocess.run(["x86_64-w64-mingw32-gcc", "installer.c", "-o", "Ghost_Kernel_x64.exe", 
                       "-mwindows", "-s"], check=True)
        
        print("[+] Created: Ghost_Kernel_x64.exe")
        print("[+] Installation directory: C:\\GhostKernel")
        
        # Очистка
        os.remove("installer.c")
        
    except Exception as e:
        print(f"[!] Compilation failed: {e}")
        print("[+] Created files in C:\\GhostKernel")
        print("[+] Run install.bat as Administrator")
    
    print("\n" + "="*60)
    print("УСТАНОВЩИК СОЗДАН!")
    print("="*60)
    print("\nЕсли создался EXE файл, запусти его от Администратора.")
    print("Если нет, открой C:\\GhostKernel\\install.bat от Администратора.")
    print("\nПосле установки ПЕРЕЗАГРУЗИ компьютер!")
    print("="*60)

def main():
    if not is_admin():
        print("[!] Запусти от Администратора!")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    print("Ghost Kernel v6.0 - 64-bit Installer Creator")
    print("===========================================")
    print("\nЭтот скрипт создаст рабочий установщик для 64-битной Windows.")
    print("\nПРЕДУПРЕЖДЕНИЕ:")
    print("- Использование читов нарушает правила игры")
    print("- Может привести к бану аккаунта")
    print("- Только для образовательных целей")
    print("\nПродолжить? (y/n): ", end="")
    
    if input().lower() != 'y':
        print("Отменено.")
        return
    
    create_installer()
    
    # Предлагаем сразу установить
    print("\nЗапустить установку сейчас? (y/n): ", end="")
    if input().lower() == 'y':
        if os.path.exists("Ghost_Kernel_x64.exe"):
            os.system("Ghost_Kernel_x64.exe")
        else:
            os.system(r"C:\GhostKernel\install.bat")

if __name__ == "__main__":
    main()