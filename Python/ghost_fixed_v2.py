# ghost_fixed_v2.py - Исправленная версия ESP
import os
import sys
import ctypes
import time
from ctypes import wintypes

# Импорты для Windows API
try:
    import win32api
    import win32con
    import win32gui
    import win32process
except ImportError:
    print("[!] Установи pywin32: pip install pywin32")
    input("Нажмите Enter для выхода...")
    sys.exit(1)

class GhostESP:
    def __init__(self):
        self.esp_active = False
        self.hotkey = "F7"  # Используем F7 вместо F11
        self.overlay_hwnd = None
        self.game_pid = None
        self.game_handle = None
        
    def create_invisible_overlay(self):
        """Создаем полностью невидимое окно-оверлей"""
        # Регистрируем класс окна
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.window_proc
        wc.lpszClassName = "GhostOverlayClass"
        wc.hbrBackground = win32gui.GetStockObject(win32con.NULL_BRUSH)
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        
        atom = win32gui.RegisterClass(wc)
        
        # Получаем размеры экрана
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        
        # Создаем окно с прозрачностью
        self.overlay_hwnd = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED |        # Для прозрачности
            win32con.WS_EX_TOPMOST |        # Поверх всех окон
            win32con.WS_EX_TRANSPARENT |    # Пропускает клики
            win32con.WS_EX_TOOLWINDOW |     # Не показывается в Alt+Tab
            win32con.WS_EX_NOACTIVATE,      # Не получает фокус
            atom,
            "Windows Input Experience",     # Маскировка под системное окно
            win32con.WS_POPUP,              # Без границ
            0, 0,                           # Позиция
            screen_width, screen_height,    # Размер на весь экран
            None, None, None, None
        )
        
        # Устанавливаем полную прозрачность (почти невидимый)
        win32gui.SetLayeredWindowAttributes(
            self.overlay_hwnd,
            0,      # Цвет ключа
            1,      # Альфа (0-255, 1 = почти невидимый)
            win32con.LWA_ALPHA
        )
        
        # Показываем окно
        win32gui.ShowWindow(self.overlay_hwnd, win32con.SW_SHOWNOACTIVATE)
        
    def window_proc(self, hwnd, msg, wparam, lparam):
        """Обработчик сообщений окна"""
        if msg == win32con.WM_HOTKEY:
            if wparam == 1:  # Наш хоткей
                self.esp_active = not self.esp_active
                print(f"[ESP] {'АКТИВИРОВАН' if self.esp_active else 'ДЕАКТИВИРОВАН'}")
                # Перерисовываем окно
                win32gui.InvalidateRect(hwnd, None, True)
                return 0
                
        elif msg == win32con.WM_PAINT:
            if self.esp_active:
                # Рисуем ESP только когда активно
                self.draw_esp(hwnd)
            else:
                # Очищаем окно
                hdc = win32gui.BeginPaint(hwnd)
                win32gui.EndPaint(hwnd, (hdc, (0,0,0,0)))
            return 0
            
        elif msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
            
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)
    
    def draw_esp(self, hwnd):
        """Рисуем ESP поверх окна"""
        # Начинаем отрисовку
        hdc = win32gui.GetDC(hwnd)
        
        try:
            # Получаем окно игры
            game_hwnd = win32gui.FindWindow("RiotWindowClass", None)
            if not game_hwnd:
                game_hwnd = win32gui.FindWindow("VALORANT", None)
            
            if game_hwnd:
                # Получаем позицию и размер окна игры
                rect = win32gui.GetWindowRect(game_hwnd)
                game_left, game_top, game_right, game_bottom = rect
                game_width = game_right - game_left
                game_height = game_bottom - game_top
                
                # Создаем красное перо
                red_pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(255, 0, 0))
                old_pen = win32gui.SelectObject(hdc, red_pen)
                
                # Рисуем крестик в центре экрана
                center_x = game_left + game_width // 2
                center_y = game_top + game_height // 2
                
                # Горизонтальная линия
                win32gui.MoveToEx(hdc, center_x - 20, center_y)
                win32gui.LineTo(hdc, center_x + 20, center_y)
                
                # Вертикальная линия
                win32gui.MoveToEx(hdc, center_x, center_y - 20)
                win32gui.LineTo(hdc, center_x, center_y + 20)
                
                # Квадрат вокруг центра
                win32gui.MoveToEx(hdc, center_x - 40, center_y - 40)
                win32gui.LineTo(hdc, center_x + 40, center_y - 40)
                win32gui.LineTo(hdc, center_x + 40, center_y + 40)
                win32gui.LineTo(hdc, center_x - 40, center_y + 40)
                win32gui.LineTo(hdc, center_x - 40, center_y - 40)
                
                # Восстанавливаем старое перо и удаляем наше
                win32gui.SelectObject(hdc, old_pen)
                win32gui.DeleteObject(red_pen)
                
                # Зеленый текст "ESP ACTIVE"
                green_brush = win32gui.CreateSolidBrush(win32api.RGB(0, 255, 0))
                old_brush = win32gui.SelectObject(hdc, green_brush)
                
                # Прямоугольник для текста
                text_rect = (game_left + 10, game_top + 10, game_left + 150, game_top + 40)
                win32gui.Rectangle(hdc, *text_rect)
                
                # Текст
                win32gui.SetBkColor(hdc, win32api.RGB(0, 255, 0))
                win32gui.SetTextColor(hdc, win32api.RGB(0, 0, 0))
                win32gui.DrawText(hdc, "ESP ACTIVE", -1, text_rect, 
                                 win32con.DT_CENTER | win32con.DT_VCENTER | win32con.DT_SINGLELINE)
                
                win32gui.SelectObject(hdc, old_brush)
                win32gui.DeleteObject(green_brush)
                
                print(f"[+] Отрисовка ESP на окне игры: {game_width}x{game_height}")
        except Exception as e:
            print(f"[!] Ошибка отрисовки: {e}")
        finally:
            win32gui.ReleaseDC(hwnd, hdc)
    
    def register_hotkey(self):
        """Регистрируем глобальный хоткей"""
        # Пробуем разные клавиши
        hotkeys = [
            (win32con.VK_F7, "F7"),
            (win32con.VK_F6, "F6"),
            (win32con.VK_F8, "F8"),
            (win32con.VK_F9, "F9")
        ]
        
        for vk_code, key_name in hotkeys:
            try:
                if win32gui.RegisterHotKey(
                    self.overlay_hwnd,
                    1,  # ID хоткея
                    0,  # Без модификаторов
                    vk_code
                ):
                    self.hotkey = key_name
                    print(f"[+] Горячая клавиша зарегистрирована: {key_name}")
                    return True
            except:
                continue
        
        print("[!] Не удалось зарегистрировать горячую клавишу")
        return False
    
    def find_game_process(self):
        """Ищем процесс Valorant"""
        PROCESS_ALL_ACCESS = 0x1F0FFF
        
        # Получаем список процессов
        processes = []
        snapshot = win32process.CreateToolhelp32Snapshot(win32con.TH32CS_SNAPPROCESS, 0)
        
        try:
            pe = win32process.Process32First(snapshot)
            while pe:
                processes.append(pe)
                pe = win32process.Process32Next(snapshot)
        except:
            pass
        finally:
            win32api.CloseHandle(snapshot)
        
        # Ищем Valorant
        target_names = [
            "VALORANT-Win64-Shipping.exe",
            "VALORANT.exe",
            "RiotClientServices.exe"
        ]
        
        for process in processes:
            for name in target_names:
                if name.lower() in process.szExeFile.decode('utf-8', errors='ignore').lower():
                    print(f"[+] Найден процесс: {process.szExeFile} (PID: {process.th32ProcessID})")
                    return process.th32ProcessID
        
        print("[!] Процесс Valorant не найден")
        return None
    
    def monitor_game(self):
        """Мониторим состояние игры"""
        while True:
            pid = self.find_game_process()
            if pid:
                if not self.game_pid:
                    print(f"[+] Игра запущена (PID: {pid})")
                    self.game_pid = pid
            else:
                if self.game_pid:
                    print("[!] Игра закрыта")
                    self.game_pid = None
                    self.esp_active = False
            
            time.sleep(2)  # Проверяем каждые 2 секунды
    
    def run(self):
        """Запуск ESP"""
        print("=" * 50)
        print("GHOST ESP - Исправленная версия v2.0")
        print("=" * 50)
        print("\nВАЖНО: Запускайте от имени Администратора!")
        print("Требуется: Python с установленным pywin32")
        print("\nИнструкция:")
        print("1. Запустите Valorant")
        print("2. Зайдите в режим тренировки или матч")
        print(f"3. Нажмите {self.hotkey} для включения/выключения ESP")
        print("\n[+] Инициализация...")
        
        # Проверяем права администратора
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            is_admin = False
            
        if not is_admin:
            print("[!] ЗАПУСТИТЕ ОТ ИМЕНИ АДМИНИСТРАТОРА!")
            print("[!] Щелкните правой кнопкой -> 'Запуск от имени администратора'")
            input("\nНажмите Enter для выхода...")
            return
        
        # Проверяем наличие игры
        print("[+] Поиск игры Valorant...")
        game_pid = self.find_game_process()
        if not game_pid:
            print("[!] Valorant не запущен")
            print("[!] Запустите игру и перезапустите ESP")
            choice = input("Всё равно продолжить? (y/n): ")
            if choice.lower() != 'y':
                return
        
        # Создаем невидимое окно
        print("[+] Создание оверлея...")
        self.create_invisible_overlay()
        
        # Регистрируем хоткей
        print("[+] Регистрация горячей клавиши...")
        if not self.register_hotkey():
            print("[!] Не удалось зарегистрировать горячую клавишу")
            print("[!] Попробуйте запустить программу снова")
            input("Нажмите Enter для выхода...")
            return
        
        # Запускаем мониторинг игры в отдельном потоке
        import threading
        monitor_thread = threading.Thread(target=self.monitor_game, daemon=True)
        monitor_thread.start()
        
        print(f"\n[+] ESP готов к работе!")
        print(f"[+] Горячая клавиша: {self.hotkey}")
        print("[+] Признак работы: красный крестик в центре экрана")
        print("[+] Текст 'ESP ACTIVE' в левом верхнем углу")
        print("\n[!] Для выхода: Alt+F4 или закройте через Диспетчер задач")
        print("=" * 50)
        
        # Главный цикл обработки сообщений
        try:
            msg = wintypes.MSG()
            while win32gui.GetMessage(ctypes.byref(msg), None, 0, 0) > 0:
                win32gui.TranslateMessage(ctypes.byref(msg))
                win32gui.DispatchMessage(ctypes.byref(msg))
                
                # Периодически обновляем окно если ESP активно
                if self.esp_active:
                    win32gui.InvalidateRect(self.overlay_hwnd, None, True)
                    win32gui.UpdateWindow(self.overlay_hwnd)
        except KeyboardInterrupt:
            print("\n[!] Прервано пользователем")
        finally:
            print("[+] Очистка...")
            if self.overlay_hwnd:
                win32gui.DestroyWindow(self.overlay_hwnd)
            print("[+] Выход")

def check_dependencies():
    """Проверяем зависимости"""
    try:
        import win32api
        import win32con
        import win32gui
        print("[+] Зависимости проверены")
        return True
    except ImportError:
        print("[!] Не установлен pywin32")
        print("[!] Установите: pip install pywin32")
        print("\nИли скачайте с официального сайта:")
        print("https://github.com/mhammond/pywin32/releases")
        return False

def create_launcher():
    """Создаем батник для запуска"""
    launcher_content = '''@echo off
title Ghost ESP Launcher
echo =======================================
echo        GHOST ESP Launcher v2.0
echo =======================================
echo.

:: Проверяем Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python не найден!
    echo [!] Установите Python 3.8+
    echo [!] Скачать: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Проверяем pywin32
python -c "import win32api" >nul 2>&1
if errorlevel 1 (
    echo [!] pywin32 не установлен!
    echo [!] Установите: pip install pywin32
    echo.
    echo Установить автоматически? (y/n)
    set /p choice=
    if /i "%choice%"=="y" (
        pip install pywin32
    ) else (
        pause
        exit /b 1
    )
)

:: Запускаем ESP
echo [+] Запуск Ghost ESP...
echo [!] Запуск от имени администратора...
echo.

:: Пытаемся запустить с повышенными привилегиями
powershell -Command "Start-Process python -ArgumentList 'ghost_fixed_v2.py' -Verb RunAs"
if errorlevel 1 (
    echo [!] Не удалось запустить с правами администратора
    echo [!] Запустите вручную: правый клик -> "Запуск от имени администратора"
    pause
)
'''
    
    with open("launch_ghost.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print("[+] Создан файл запуска: launch_ghost.bat")

def main():
    """Главная функция"""
    print("Ghost ESP - Установка и запуск")
    print("=" * 40)
    print("\nВыберите опцию:")
    print("1. Проверить зависимости")
    print("2. Создать ярлык для запуска")
    print("3. Запустить Ghost ESP")
    print("4. Выход")
    
    try:
        choice = input("\nВаш выбор (1-4): ").strip()
        
        if choice == "1":
            # Проверка зависимостей
            if check_dependencies():
                print("\n[+] Все зависимости установлены!")
                print("[+] Можно запускать ESP")
            input("\nНажмите Enter для продолжения...")
            main()
            
        elif choice == "2":
            # Создаем ярлык
            create_launcher()
            print("\n[+] Запустите launch_ghost.bat для запуска ESP")
            input("\nНажмите Enter для продолжения...")
            main()
            
        elif choice == "3":
            # Запускаем ESP
            if not check_dependencies():
                input("\nНажмите Enter для выхода...")
                return
            
            print("\n[+] Запуск Ghost ESP...")
            print("[!] Убедитесь что Valorant запущен!")
            input("\nНажмите Enter для продолжения...")
            
            esp = GhostESP()
            esp.run()
            
        elif choice == "4":
            print("[+] Выход")
            return
            
        else:
            print("[!] Неверный выбор")
            main()
            
    except KeyboardInterrupt:
        print("\n[!] Прервано пользователем")
    except Exception as e:
        print(f"[!] Ошибка: {e}")
        input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()