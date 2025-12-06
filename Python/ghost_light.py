# ghost_light.py - ESP без зависимостей от pywin32
import os
import sys
import time
import ctypes
from ctypes import wintypes, windll, byref, c_int, c_uint, c_char_p, c_void_p

# Константы Windows
HWND_TOPMOST = -1
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
WS_EX_LAYERED = 0x80000
WS_EX_TRANSPARENT = 0x20
WS_EX_TOOLWINDOW = 0x80
WS_POPUP = 0x80000000
WM_PAINT = 0x000F
WM_HOTKEY = 0x0312
VK_F7 = 0x76
VK_F6 = 0x75
MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
COLOR_WINDOW = 5

class GhostESPLight:
    def __init__(self):
        self.esp_active = False
        self.hotkey = VK_F7
        self.hwnd = None
        self.game_pid = 0
        
        # Загружаем необходимые функции
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        self.gdi32 = ctypes.windll.gdi32
        
    def create_window(self):
        """Создаем невидимое окно чистыми WinAPI вызовами"""
        # Регистрируем класс окна
        wnd_class = wintypes.WNDCLASSEX()
        wnd_class.cbSize = ctypes.sizeof(wintypes.WNDCLASSEX)
        wnd_class.lpfnWndProc = self.window_proc
        wnd_class.hInstance = self.kernel32.GetModuleHandleW(None)
        wnd_class.lpszClassName = "GhostOverlay"
        wnd_class.hbrBackground = self.user32.GetStockObject(COLOR_WINDOW)
        wnd_class.hCursor = self.user32.LoadCursorW(0, 32512)  # IDC_ARROW
        
        atom = self.user32.RegisterClassExW(byref(wnd_class))
        
        # Создаем окно
        self.hwnd = self.user32.CreateWindowExW(
            WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW,
            atom,
            "Windows Input Experience",
            WS_POPUP,
            0, 0,  # x, y
            self.user32.GetSystemMetrics(0),  # SM_CXSCREEN
            self.user32.GetSystemMetrics(1),  # SM_CYSCREEN
            0, 0, wnd_class.hInstance, None
        )
        
        # Устанавливаем прозрачность
        self.user32.SetLayeredWindowAttributes(
            self.hwnd,
            0,  # Color key
            1,  # Alpha (1 = почти невидимый)
            0x00000002  # LWA_ALPHA
        )
        
        # Делаем окно поверх всех
        self.user32.SetWindowPos(
            self.hwnd,
            HWND_TOPMOST,
            0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE
        )
        
        # Показываем окно
        self.user32.ShowWindow(self.hwnd, 1)
        
    def window_proc(self, hwnd, msg, wparam, lparam):
        """Процедура окна"""
        if msg == WM_HOTKEY:
            if wparam == 1:
                self.esp_active = not self.esp_active
                print(f"[ESP] {'ВКЛ' if self.esp_active else 'ВЫКЛ'}")
                # Перерисовываем окно
                self.user32.InvalidateRect(hwnd, None, True)
                
        elif msg == WM_PAINT and self.esp_active:
            # Рисуем ESP
            self.draw_esp(hwnd)
            
        elif msg == 2:  # WM_DESTROY
            self.user32.PostQuitMessage(0)
            
        return self.user32.DefWindowProcW(hwnd, msg, wparam, lparam)
    
    def draw_esp(self, hwnd):
        """Рисуем простой ESP"""
        # Получаем контекст устройства
        hdc = wintypes.HDC()
        ps = wintypes.PAINTSTRUCT()
        hdc.value = self.user32.BeginPaint(hwnd, byref(ps))
        
        if hdc.value:
            # Создаем красное перо
            pen = self.gdi32.CreatePen(0, 2, 0x0000FF)  # Красный цвет
            old_pen = self.gdi32.SelectObject(hdc, pen)
            
            # Получаем размеры экрана
            screen_w = self.user32.GetSystemMetrics(0)
            screen_h = self.user32.GetSystemMetrics(1)
            
            # Рисуем крестик в центре
            center_x = screen_w // 2
            center_y = screen_h // 2
            
            # Вертикальная линия
            self.gdi32.MoveToEx(hdc, center_x, center_y - 20, None)
            self.gdi32.LineTo(hdc, center_x, center_y + 20)
            
            # Горизонтальная линия
            self.gdi32.MoveToEx(hdc, center_x - 20, center_y, None)
            self.gdi32.LineTo(hdc, center_x + 20, center_y)
            
            # Восстанавливаем старое перо
            self.gdi32.SelectObject(hdc, old_pen)
            self.gdi32.DeleteObject(pen)
            
            # Если игра найдена, рисуем больше
            if self.game_pid:
                # Рисуем рамку
                brush = self.gdi32.GetStockObject(0)  # NULL_BRUSH
                old_brush = self.gdi32.SelectObject(hdc, brush)
                
                self.gdi32.Rectangle(hdc, 
                                   center_x - 100, center_y - 100,
                                   center_x + 100, center_y + 100)
                
                self.gdi32.SelectObject(hdc, old_brush)
            
            self.user32.EndPaint(hwnd, byref(ps))
    
    def find_valorant(self):
        """Ищем процесс Valorant без win32process"""
        PROCESS_QUERY_INFORMATION = 0x0400
        PROCESS_VM_READ = 0x0010
        
        # Создаем снимок процессов
        TH32CS_SNAPPROCESS = 0x00000002
        snapshot = self.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        
        if snapshot == -1:
            return 0
        
        class PROCESSENTRY32(ctypes.Structure):
            _fields_ = [
                ("dwSize", wintypes.DWORD),
                ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD),
                ("th32DefaultHeapID", wintypes.ULONG),
                ("th32ModuleID", wintypes.DWORD),
                ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD),
                ("pcPriClassBase", wintypes.LONG),
                ("dwFlags", wintypes.DWORD),
                ("szExeFile", ctypes.c_char * 260)
            ]
        
        pe32 = PROCESSENTRY32()
        pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)
        
        if self.kernel32.Process32First(snapshot, ctypes.byref(pe32)):
            while self.kernel32.Process32Next(snapshot, ctypes.byref(pe32)):
                exe_name = pe32.szExeFile.decode('utf-8', errors='ignore')
                if "VALORANT" in exe_name.upper() or "VALORANT-WIN64" in exe_name.upper():
                    self.game_pid = pe32.th32ProcessID
                    print(f"[+] Найден Valorant: PID {self.game_pid}")
                    break
        
        self.kernel32.CloseHandle(snapshot)
        return self.game_pid
    
    def register_hotkey(self):
        """Регистрируем горячую клавишу"""
        # Пробуем F7
        if self.user32.RegisterHotKey(self.hwnd, 1, 0, VK_F7):
            print("[+] Горячая клавиша: F7")
            return True
        else:
            # Пробуем F6
            if self.user32.RegisterHotKey(self.hwnd, 1, 0, VK_F6):
                print("[+] Горячая клавиша: F6")
                self.hotkey = VK_F6
                return True
        
        print("[!] Не удалось зарегистрировать горячую клавишу")
        return False
    
    def run_message_loop(self):
        """Запускаем цикл сообщений"""
        msg = wintypes.MSG()
        while self.user32.GetMessageW(byref(msg), None, 0, 0):
            self.user32.TranslateMessage(byref(msg))
            self.user32.DispatchMessageW(byref(msg))
            
            # Периодически ищем игру
            if int(time.time()) % 10 == 0:
                if not self.game_pid:
                    self.find_valorant()
    
    def run(self):
        """Запуск ESP"""
        print("=" * 50)
        print("GHOST ESP LIGHT v1.0")
        print("=" * 50)
        print("[+] Создание окна...")
        
        # Создаем окно
        self.create_window()
        
        print("[+] Регистрация горячей клавиши...")
        if not self.register_hotkey():
            print("[!] Используйте Alt+F4 для выхода")
        
        print("[+] Поиск Valorant...")
        self.find_valorant()
        
        print("\n" + "=" * 50)
        print("ИНСТРУКЦИЯ:")
        print("1. Запустите Valorant (если еще не запущен)")
        print("2. Зайдите в матч или режим тренировки")
        print("3. Нажмите F7 (или F6) для включения ESP")
        print("4. Красный крестик в центре = ESP работает")
        print("5. Снова F7/F6 для выключения")
        print("\n[!] Для выхода закройте это окно")
        print("=" * 50)
        
        # Запускаем цикл сообщений
        self.run_message_loop()

def check_python():
    """Проверяем наличие Python"""
    print("[+] Проверка Python...")
    
    # Проверяем версию
    if sys.version_info.major < 3:
        print("[!] Требуется Python 3.x")
        return False
    
    print(f"[+] Python {sys.version_info.major}.{sys.version_info.minor} обнаружен")
    return True

def create_launcher():
    """Создаем launcher.bat для запуска"""
    launcher_content = '''@echo off
chcp 65001 >nul
title Ghost ESP Launcher

echo ===============================
echo      GHOST ESP LIGHT v1.0
echo ===============================
echo.

echo [!] Убедитесь что:
echo     1. Valorant ЗАПУЩЕН
echo     2. Вы в матче или режиме тренировки
echo     3. Нажмите F7 в игре для активации
echo.

echo [1] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python не найден!
    echo [!] Скачайте с python.org
    pause
    exit /b 1
)

echo [2] Запуск ESP...
echo [!] Не закрывайте это окно!
echo [!] Нажмите F7 в игре для активации
echo.

python "%~dp0ghost_light.py"
pause
'''
    
    with open("launch_ghost.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    return "launch_ghost.bat"

def create_desktop_shortcut():
    """Создаем ярлык на рабочем столе"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "Ghost ESP.lnk")
        
        target = os.path.join(os.getcwd(), "launch_ghost.bat")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = "shell32.dll,1"
        shortcut.save()
        
        return True
    except:
        return False

def main():
    """Главная функция"""
    print("[+] Инициализация Ghost ESP...")
    
    # Проверяем Python
    if not check_python():
        input("Нажмите Enter для выхода...")
        return
    
    # Создаем launcher
    launcher = create_launcher()
    print(f"[+] Создан запускатель: {launcher}")
    
    # Предлагаем создать ярлык
    print("\nСоздать ярлык на рабочем столе? (y/n): ", end="")
    if input().lower() == 'y':
        if create_desktop_shortcut():
            print("[+] Ярлык создан на рабочем столе")
        else:
            print("[!] Не удалось создать ярлык")
    
    # Запускаем ESP или показываем инструкцию
    print("\n" + "=" * 50)
    print("ВЫБЕРИТЕ ДЕЙСТВИЕ:")
    print("1. Запустить Ghost ESP сейчас (нужен запущенный Valorant)")
    print("2. Только создать файлы, запустить позже")
    print("=" * 50)
    
    choice = input("Ваш выбор (1-2): ")
    
    if choice == "1":
        print("\n[+] Запуск Ghost ESP...")
        print("[!] Убедитесь что Valorant запущен!")
        input("Нажмите Enter чтобы продолжить...")
        
        esp = GhostESPLight()
        esp.run()
    else:
        print("\n" + "=" * 50)
        print("ФАЙЛЫ СОЗДАНЫ:")
        print(f"1. ghost_light.py - основной файл ESP")
        print(f"2. {launcher} - запускатель")
        print("\nКАК ИСПОЛЬЗОВАТЬ:")
        print("1. Запустите Valorant и зайдите в матч")
        print(f"2. Запустите {launcher} от Администратора")
        print("3. Нажмите F7 в игре для активации ESP")
        print("4. Красный крестик = ESP работает")
        print("=" * 50)
        input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    # Проверяем права администратора
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        is_admin = False
    
    if not is_admin:
        print("[!] Запустите от имени Администратора!")
        print("[!] Правый клик -> Запуск от имени администратора")
        input("Нажмите Enter для выхода...")
        sys.exit(1)
    
    main()