# ghost_simple.py - Максимально простой ESP без зависимостей
import os
import sys
import time
import ctypes
from ctypes import *

# Простые константы
VK_F7 = 0x76
VK_F8 = 0x77
COLOR_RED = 0x0000FF

class SimpleESP:
    def __init__(self):
        self.esp_active = False
        self.user32 = windll.user32
        self.gdi32 = windll.gdi32
        self.kernel32 = windll.kernel32
        self.hwnd = None
        
    def find_valorant_window(self):
        """Ищем окно Valorant"""
        def enum_windows_callback(hwnd, lparam):
            length = self.user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buffer = create_unicode_buffer(length + 1)
                self.user32.GetWindowTextW(hwnd, buffer, length + 1)
                title = buffer.value
                
                # Ищем окно Valorant
                if "VALORANT" in title.upper() or "RIOT" in title.upper():
                    # Сохраняем handle окна
                    if not lparam:
                        nonlocal game_hwnd
                        game_hwnd = hwnd
                    return False
            return True
        
        game_hwnd = None
        WNDENUMPROC = WINFUNCTYPE(c_bool, c_void_p, c_void_p)
        self.user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)
        
        return game_hwnd
    
    def draw_overlay(self):
        """Рисуем оверлей поверх экрана"""
        # Получаем handle всего экрана
        hdc = self.user32.GetDC(0)
        
        if hdc:
            # Создаем красное перо
            pen = self.gdi32.CreatePen(0, 2, COLOR_RED)
            old_pen = self.gdi32.SelectObject(hdc, pen)
            
            # Получаем размеры экрана
            screen_w = self.user32.GetSystemMetrics(0)  # SM_CXSCREEN
            screen_h = self.user32.GetSystemMetrics(1)  # SM_CYSCREEN
            
            # Рисуем крестик в центре
            center_x = screen_w // 2
            center_y = screen_h // 2
            
            # Вертикальная линия
            self.gdi32.MoveToEx(hdc, center_x, center_y - 20, None)
            self.gdi32.LineTo(hdc, center_x, center_y + 20)
            
            # Горизонтальная линия
            self.gdi32.MoveToEx(hdc, center_x - 20, center_y, None)
            self.gdi32.LineTo(hdc, center_x + 20, center_y)
            
            # Квадрат вокруг центра
            self.gdi32.Rectangle(hdc, 
                               center_x - 100, center_y - 100,
                               center_x + 100, center_y + 100)
            
            # Если нашли Valorant, рисуем дополнительную информацию
            game_hwnd = self.find_valorant_window()
            if game_hwnd:
                # Рисуем текст в углу
                font = self.gdi32.CreateFontW(
                    20, 0, 0, 0, 400,  # Высота, вес
                    False, False, False,  # Курсив, подчеркивание, зачеркивание
                    0, 0, 0, 0,  # Кодировка, качество
                    "Arial"
                )
                old_font = self.gdi32.SelectObject(hdc, font)
                
                self.gdi32.SetTextColor(hdc, COLOR_RED)
                self.gdi32.SetBkMode(hdc, 1)  # TRANSPARENT
                
                text = "ESP ACTIVE - F8 TOGGLE"
                self.gdi32.TextOutW(hdc, 10, 10, text, len(text))
                
                self.gdi32.SelectObject(hdc, old_font)
                self.gdi32.DeleteObject(font)
            
            # Восстанавливаем и удаляем перо
            self.gdi32.SelectObject(hdc, old_pen)
            self.gdi32.DeleteObject(pen)
            
            # Освобождаем контекст устройства
            self.user32.ReleaseDC(0, hdc)
    
    def clear_overlay(self):
        """Очищаем оверлей (перерисовываем экран)"""
        # Просим Windows перерисовать весь экран
        self.user32.RedrawWindow(0, None, 0, 0x0405)  # RDW_INVALIDATE | RDW_ALLCHILDREN
    
    def check_hotkey(self):
        """Проверяем нажатие горячей клавиши"""
        # Проверяем F7
        if self.user32.GetAsyncKeyState(VK_F7) & 0x8000:
            return "F7"
        # Проверяем F8  
        elif self.user32.GetAsyncKeyState(VK_F8) & 0x8000:
            return "F8"
        return None
    
    def run(self):
        """Запуск ESP"""
        print("=" * 60)
        print("SIMPLE GHOST ESP v1.0")
        print("=" * 60)
        print("[+] Поиск Valorant...")
        
        # Ищем Valorant
        game_hwnd = self.find_valorant_window()
        if game_hwnd:
            print(f"[+] Valorant найден (handle: {game_hwnd})")
        else:
            print("[!] Valorant не найден")
            print("[!] Запустите Valorant для лучшей работы ESP")
        
        print("\n" + "=" * 60)
        print("ИНСТРУКЦИЯ:")
        print("1. Не закрывайте это окно")
        print("2. Переключитесь в Valorant (Alt+Tab)")
        print("3. Нажмите F8 для включения ESP")
        print("4. Красный крестик в центре = ESP работает")
        print("5. Снова F8 для выключения")
        print("=" * 60)
        print("\n[+] ESP запущен. Нажмите Ctrl+C в этом окне для выхода.")
        
        last_key_time = 0
        key_delay = 0.3  # Задержка между нажатиями
        
        try:
            while True:
                # Проверяем горячие клавиши
                current_time = time.time()
                if current_time - last_key_time > key_delay:
                    hotkey = self.check_hotkey()
                    
                    if hotkey:
                        last_key_time = current_time
                        
                        if hotkey == "F7" or hotkey == "F8":
                            self.esp_active = not self.esp_active
                            
                            if self.esp_active:
                                print(f"[+] ESP АКТИВИРОВАН ({hotkey})")
                            else:
                                print(f"[+] ESP ВЫКЛЮЧЕН ({hotkey})")
                                self.clear_overlay()
                
                # Если ESP активно, рисуем оверлей
                if self.esp_active:
                    self.draw_overlay()
                
                # Небольшая задержка для снижения нагрузки на CPU
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\n[+] ESP остановлен")
            self.clear_overlay()
        except Exception as e:
            print(f"[!] Ошибка: {e}")
            self.clear_overlay()

def create_launcher_bat():
    """Создаем батник для запуска"""
    bat_content = '''@echo off
chcp 65001 >nul
title Simple Ghost ESP

echo ====================================
echo       SIMPLE GHOST ESP v1.0
echo ====================================
echo.

echo [!] ТРЕБОВАНИЯ:
echo     1. Запустите от имени Администратора
echo     2. Valorant должен быть запущен
echo     3. Вы в матче или режиме тренировки
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
echo [!] Нажмите F8 в игре для активации
echo.

python "%~dp0ghost_simple.py"
pause
'''
    
    with open("run_esp.bat", "w", encoding="utf-8") as f:
        f.write(bat_content)
    
    return "run_esp.bat"

def check_admin():
    """Проверяем права администратора"""
    try:
        return windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def main():
    """Главная функция"""
    print("[+] Simple Ghost ESP - Инициализация...")
    
    # Проверяем права
    if not check_admin():
        print("[!] ЗАПУСТИТЕ ОТ ИМЕНИ АДМИНИСТРАТОРА!")
        print("[!] Правый клик -> 'Запуск от имени администратора'")
        input("Нажмите Enter для выхода...")
        return
    
    # Проверяем Python
    if sys.version_info.major < 3:
        print("[!] Требуется Python 3.x")
        input("Нажмите Enter для выхода...")
        return
    
    print(f"[+] Python {sys.version_info.major}.{sys.version_info.minor} обнаружен")
    
    # Создаем launcher
    launcher = create_launcher_bat()
    print(f"[+] Создан запускатель: {launcher}")
    
    # Инструкция
    print("\n" + "=" * 60)
    print("ИНСТРУКЦИЯ ПО ЗАПУСКУ:")
    print(f"1. Запустите {launcher} от Администратора")
    print("2. Запустите Valorant и зайдите в матч")
    print("3. Нажмите F8 в игре для активации")
    print("4. Красный крестик в центре = ESP работает")
    print("=" * 60)
    
    # Сразу запускаем ESP
    print("\n[+] Запуск ESP через 3 секунды...")
    print("[!] Убедитесь что Valorant запущен!")
    
    for i in range(3, 0, -1):
        print(f"[{i}]...")
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("ESP ЗАПУЩЕН!")
    print("Переключитесь в Valorant (Alt+Tab)")
    print("Нажмите F8 для включения/выключения")
    print("=" * 60)
    
    # Запускаем ESP
    esp = SimpleESP()
    esp.run()

if __name__ == "__main__":
    main()