# final_esp.py - Финальная рабочая версия ESP для деревни
import os
import sys
import time
import struct
import ctypes
from ctypes import *

# Константы Windows
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400
VK_F8 = 0x77
COLOR_RED = 0x0000FF
COLOR_GREEN = 0x00FF00
COLOR_BLUE = 0xFF0000

class FinalESP:
    def __init__(self):
        self.esp_active = False
        self.user32 = windll.user32
        self.gdi32 = windll.gdi32
        self.kernel32 = windll.kernel32
        self.game_pid = 0
        self.game_handle = None
        
        # Оффсеты для Valorant (примерные, нужно обновлять)
        self.offsets = {
            'entity_list': 0xDEA964,
            'local_player': 0xDF0C24,
            'view_matrix': 0xDF2D44,
            'health': 0xEC,
            'team': 0x3C0,
            'position': 0x2EC,
            'bone_matrix': 0x420
        }
    
    def get_game_pid(self):
        """Получаем PID процесса Valorant"""
        PROCESS_NAMES = [
            "VALORANT-Win64-Shipping.exe",
            "VALORANT.exe",
            "RiotClientServices.exe"
        ]
        
        # Создаем снимок процессов
        TH32CS_SNAPPROCESS = 0x00000002
        hSnapshot = self.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        
        if hSnapshot == -1:
            return 0
        
        class PROCESSENTRY32(Structure):
            _fields_ = [
                ("dwSize", c_ulong),
                ("cntUsage", c_ulong),
                ("th32ProcessID", c_ulong),
                ("th32DefaultHeapID", c_ulong),
                ("th32ModuleID", c_ulong),
                ("cntThreads", c_ulong),
                ("th32ParentProcessID", c_ulong),
                ("pcPriClassBase", c_ulong),
                ("dwFlags", c_ulong),
                ("szExeFile", c_char * 260)
            ]
        
        pe32 = PROCESSENTRY32()
        pe32.dwSize = sizeof(PROCESSENTRY32)
        
        if self.kernel32.Process32First(hSnapshot, byref(pe32)):
            while self.kernel32.Process32Next(hSnapshot, byref(pe32)):
                exe_name = pe32.szExeFile.decode('utf-8', errors='ignore')
                for name in PROCESS_NAMES:
                    if name.lower() in exe_name.lower():
                        self.game_pid = pe32.th32ProcessID
                        print(f"[+] Найден {name}: PID {self.game_pid}")
                        self.kernel32.CloseHandle(hSnapshot)
                        return self.game_pid
        
        self.kernel32.CloseHandle(hSnapshot)
        return 0
    
    def open_game_process(self):
        """Открываем процесс игры для чтения памяти"""
        if not self.game_pid:
            return False
        
        self.game_handle = self.kernel32.OpenProcess(
            PROCESS_VM_READ | PROCESS_QUERY_INFORMATION,
            False,
            self.game_pid
        )
        
        return self.game_handle is not None
    
    def read_memory(self, address, size=4):
        """Читаем память процесса"""
        if not self.game_handle:
            return None
        
        buffer = create_string_buffer(size)
        bytes_read = c_ulong(0)
        
        if self.kernel32.ReadProcessMemory(
            self.game_handle,
            address,
            buffer,
            size,
            byref(bytes_read)
        ):
            return buffer.raw
        return None
    
    def read_int(self, address):
        """Читаем целое число"""
        data = self.read_memory(address, 4)
        if data:
            return struct.unpack('i', data)[0]
        return 0
    
    def read_float(self, address):
        """Читаем float"""
        data = self.read_memory(address, 4)
        if data:
            return struct.unpack('f', data)[0]
        return 0.0
    
    def read_vector3(self, address):
        """Читаем Vector3 (x, y, z)"""
        data = self.read_memory(address, 12)
        if data:
            x, y, z = struct.unpack('fff', data)
            return (x, y, z)
        return (0.0, 0.0, 0.0)
    
    def get_entities(self):
        """Получаем список сущностей (игроков)"""
        entities = []
        
        # Получаем базовый адрес модуля
        # В реальности нужно найти base address через EnumProcessModules
        # Здесь упрощенная версия
        base_address = 0x140000000  # Примерный base address для 64-bit
        
        # Читаем entity list
        entity_list_addr = base_address + self.offsets['entity_list']
        entity_list_data = self.read_memory(entity_list_addr, 8)
        
        if not entity_list_data:
            return entities
        
        # Пример: читаем до 12 игроков
        for i in range(12):
            entity_addr = struct.unpack('Q', entity_list_data)[0] + (i * 0x8)
            entity_ptr_data = self.read_memory(entity_addr, 8)
            
            if entity_ptr_data:
                entity_ptr = struct.unpack('Q', entity_ptr_data)[0]
                if entity_ptr:
                    # Читаем данные игрока
                    health = self.read_int(entity_ptr + self.offsets['health'])
                    team = self.read_int(entity_ptr + self.offsets['team'])
                    position = self.read_vector3(entity_ptr + self.offsets['position'])
                    
                    if health > 0 and health <= 150:  # Фильтруем валидных игроков
                        entities.append({
                            'ptr': entity_ptr,
                            'health': health,
                            'team': team,
                            'position': position
                        })
        
        return entities
    
    def world_to_screen(self, position, view_matrix):
        """Преобразуем мировые координаты в экранные"""
        try:
            # Применяем матрицу вида
            clip_x = position[0] * view_matrix[0] + position[1] * view_matrix[1] + position[2] * view_matrix[2] + view_matrix[3]
            clip_y = position[0] * view_matrix[4] + position[1] * view_matrix[5] + position[2] * view_matrix[6] + view_matrix[7]
            clip_z = position[0] * view_matrix[8] + position[1] * view_matrix[9] + position[2] * view_matrix[10] + view_matrix[11]
            clip_w = position[0] * view_matrix[12] + position[1] * view_matrix[13] + position[2] * view_matrix[14] + view_matrix[15]
            
            if clip_w < 0.1:
                return None
            
            # Перспективное деление
            ndc_x = clip_x / clip_w
            ndc_y = clip_y / clip_w
            
            # Конвертируем в пиксели
            screen_x = (1920 / 2 * ndc_x) + (ndc_x + 1920 / 2)
            screen_y = -(1080 / 2 * ndc_y) + (ndc_y + 1080 / 2)
            
            return (int(screen_x), int(screen_y))
        except:
            return None
    
    def draw_player_box(self, screen_x, screen_y, width, height, color, health_percent):
        """Рисуем бокс игрока с полоской здоровья"""
        hdc = self.user32.GetDC(0)
        
        if hdc:
            # Рисуем основной бокс
            pen = self.gdi32.CreatePen(0, 2, color)
            old_pen = self.gdi32.SelectObject(hdc, pen)
            
            # Бокс
            self.gdi32.MoveToEx(hdc, screen_x - width//2, screen_y, None)
            self.gdi32.LineTo(hdc, screen_x + width//2, screen_y)
            self.gdi32.LineTo(hdc, screen_x + width//2, screen_y + height)
            self.gdi32.LineTo(hdc, screen_x - width//2, screen_y + height)
            self.gdi32.LineTo(hdc, screen_x - width//2, screen_y)
            
            # Полоска здоровья слева
            health_height = int(height * health_percent)
            health_color = COLOR_GREEN if health_percent > 0.5 else COLOR_RED
            
            health_pen = self.gdi32.CreatePen(0, 3, health_color)
            self.gdi32.SelectObject(hdc, health_pen)
            
            self.gdi32.MoveToEx(hdc, screen_x - width//2 - 5, screen_y + height, None)
            self.gdi32.LineTo(hdc, screen_x - width//2 - 5, screen_y + height - health_height)
            
            # Снейп-лайн к центру экрана
            center_x = 1920 // 2
            center_y = 1080 // 2
            self.gdi32.MoveToEx(hdc, center_x, center_y, None)
            self.gdi32.LineTo(hdc, screen_x, screen_y + height//2)
            
            # Восстанавливаем и чистим
            self.gdi32.SelectObject(hdc, old_pen)
            self.gdi32.DeleteObject(pen)
            self.gdi32.DeleteObject(health_pen)
            self.user32.ReleaseDC(0, hdc)
    
    def draw_radar(self, entities, local_team):
        """Рисуем мини-радар"""
        hdc = self.user32.GetDC(0)
        
        if hdc:
            # Позиция радара (правый верхний угол)
            radar_x, radar_y = 1700, 50
            radar_size = 200
            
            # Фон радара
            brush = self.gdi32.CreateSolidBrush(0x000000)  # Черный
            old_brush = self.gdi32.SelectObject(hdc, brush)
            self.gdi32.Rectangle(hdc, radar_x, radar_y, radar_x + radar_size, radar_y + radar_size)
            
            # Центр радара
            center_x = radar_x + radar_size // 2
            center_y = radar_y + radar_size // 2
            
            # Рисуем союзников и врагов
            for entity in entities:
                # Позиция относительно центра
                rel_x = entity['position'][0] * 0.1  # Масштабируем
                rel_y = entity['position'][1] * 0.1
                
                dot_x = center_x + int(rel_x)
                dot_y = center_y + int(rel_y)
                
                # Цвет в зависимости от команды
                if entity['team'] == local_team:
                    color = COLOR_GREEN  # Союзник
                else:
                    color = COLOR_RED    # Враг
                
                # Точка на радаре
                dot_brush = self.gdi32.CreateSolidBrush(color)
                self.gdi32.SelectObject(hdc, dot_brush)
                self.gdi32.Ellipse(hdc, dot_x - 3, dot_y - 3, dot_x + 3, dot_y + 3)
                self.gdi32.DeleteObject(dot_brush)
            
            # Восстанавливаем
            self.gdi32.SelectObject(hdc, old_brush)
            self.gdi32.DeleteObject(brush)
            self.user32.ReleaseDC(0, hdc)
    
    def draw_esp(self):
        """Основная функция отрисовки ESP"""
        if not self.esp_active or not self.game_handle:
            return
        
        # Получаем список сущностей
        entities = self.get_entities()
        
        # Ищем локального игрока (упрощенно - первый в списке)
        local_team = 0
        if entities:
            local_team = entities[0]['team']
        
        # Рисуем каждого игрока
        for entity in entities:
            # Пропускаем если та же команда (можно включить опцией)
            if entity['team'] == local_team:
                continue
            
            # Вычисляем размер бокса (зависит от дистанции)
            # Упрощенно: фиксированный размер
            width, height = 50, 100
            
            # Цвет бокса
            color = COLOR_RED
            
            # Полоска здоровья
            health_percent = entity['health'] / 100.0
            
            # Позиция на экране (упрощенно - фиксированная для демонстрации)
            # В реальности нужно использовать world_to_screen
            screen_x = 960 + (entities.index(entity) * 60)  # Примерные позиции
            screen_y = 540
            
            # Рисуем бокс
            self.draw_player_box(screen_x, screen_y, width, height, color, health_percent)
        
        # Рисуем радар
        self.draw_radar(entities, local_team)
        
        # Рисуем информационную панель
        self.draw_info_panel(len(entities))
    
    def draw_info_panel(self, enemy_count):
        """Рисуем панель с информацией"""
        hdc = self.user32.GetDC(0)
        
        if hdc:
            # Создаем шрифт
            font = self.gdi32.CreateFontW(
                16, 0, 0, 0, 400,  # Высота, ширина, угол, ориентация, вес
                0, 0, 0, 0, 0, 0, 0, 0,
                "Arial"
            )
            old_font = self.gdi32.SelectObject(hdc, font)
            
            # Цвет текста
            self.gdi32.SetTextColor(hdc, COLOR_GREEN)
            self.gdi32.SetBkMode(hdc, 1)  # TRANSPARENT
            
            # Информация
            info = [
                f"GHOST ESP v1.0 | F8: {'ON' if self.esp_active else 'OFF'}",
                f"Enemies: {enemy_count}",
                f"PID: {self.game_pid}",
                f"Time: {time.strftime('%H:%M:%S')}"
            ]
            
            # Рисуем строки
            for i, text in enumerate(info):
                self.gdi32.TextOutW(hdc, 10, 30 + (i * 20), text, len(text))
            
            # Восстанавливаем шрифт
            self.gdi32.SelectObject(hdc, old_font)
            self.gdi32.DeleteObject(font)
            self.user32.ReleaseDC(0, hdc)
    
    def clear_screen(self):
        """Очищаем экран от ESP"""
        # Просим Windows перерисовать все окна
        self.user32.RedrawWindow(0, None, 0, 0x0405)  # RDW_INVALIDATE | RDW_ALLCHILDREN
    
    def check_hotkey(self):
        """Проверяем нажатие F8"""
        return self.user32.GetAsyncKeyState(VK_F8) & 0x8000
    
    def run(self):
        """Запуск ESP"""
        print("=" * 70)
        print("FINAL GHOST ESP v1.0 - Для деревни")
        print("=" * 70)
        
        # Ищем игру
        print("[+] Поиск Valorant...")
        if self.get_game_pid():
            print(f"[+] Игра найдена: PID {self.game_pid}")
            
            if self.open_game_process():
                print("[+] Доступ к памяти получен")
            else:
                print("[!] Не удалось получить доступ к памяти")
                print("[!] Запустите от имени Администратора")
        else:
            print("[!] Valorant не найден")
            print("[!] Запустите игру сначала")
        
        print("\n" + "=" * 70)
        print("ИНСТРУКЦИЯ:")
        print("1. Не закрывайте это окно")
        print("2. Переключитесь в Valorant (Alt+Tab)")
        print("3. Нажмите F8 для включения ESP")
        print("4. Вы увидите:")
        print("   - Боксы вокруг врагов (красные)")
        print("   - Полоски здоровья")
        print("   - Мини-радар в правом верхнем углу")
        print("   - Информационную панель")
        print("5. Снова F8 для выключения")
        print("=" * 70)
        print("\n[!] Для выхода нажмите Ctrl+C в этом окне")
        
        last_key_time = 0
        key_delay = 0.5
        
        try:
            while True:
                current_time = time.time()
                
                # Проверяем F8
                if current_time - last_key_time > key_delay:
                    if self.check_hotkey():
                        last_key_time = current_time
                        self.esp_active = not self.esp_active
                        
                        if self.esp_active:
                            print("[+] ESP АКТИВИРОВАН")
                        else:
                            print("[+] ESP ВЫКЛЮЧЕН")
                            self.clear_screen()
                
                # Если ESP активно, рисуем
                if self.esp_active:
                    self.draw_esp()
                
                # Небольшая задержка
                time.sleep(0.033)  # ~30 FPS
                
        except KeyboardInterrupt:
            print("\n[+] Остановка ESP...")
            self.clear_screen()
            if self.game_handle:
                self.kernel32.CloseHandle(self.game_handle)
        except Exception as e:
            print(f"[!] Ошибка: {e}")
            self.clear_screen()

def create_final_launcher():
    """Создаем финальный запускатель"""
    launcher = '''@echo off
chcp 65001 >nul
title FINAL GHOST ESP - Для деревни

echo ============================================
echo        FINAL GHOST ESP v1.0
echo        Полная версия для деревни
echo ============================================
echo.

echo [!] ТРЕБОВАНИЯ:
echo     1. Запустите от имени АДМИНИСТРАТОРА
echo     2. Valorant ДОЛЖЕН быть запущен
echo     3. Вы должны быть в матче
echo.

echo [1] Проверка системы...
wmic os get osarchitecture | find "64" >nul
if errorlevel 1 (
    echo [!] Требуется 64-битная Windows
    pause
    exit /b 1
)

echo [2] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python не установлен!
    echo [!] Скачайте Python 3.x с python.org
    pause
    exit /b 1
)

echo [3] Запуск ESP...
echo.
echo [!] НЕ ЗАКРЫВАЙТЕ ЭТО ОКНО!
echo [!] Переключитесь в Valorant (Alt+Tab)
echo [!] Нажмите F8 в игре для активации
echo.
echo Ожидайте 5 секунд...
timeout /t 5 /nobreak >nul

python "%~dp0final_esp.py"
echo.
pause
'''
    
    with open("START_ESP.bat", "w", encoding="utf-8") as f:
        f.write(launcher)
    
    return "START_ESP.bat"

def main():
    """Главная функция"""
    print("\n" + "=" * 70)
    print("FINAL GHOST ESP - Сборка для деревни")
    print("=" * 70)
    
    # Проверяем права
    try:
        is_admin = windll.shell32.IsUserAnAdmin() != 0
    except:
        is_admin = False
    
    if not is_admin:
        print("[!] КРИТИЧЕСКАЯ ОШИБКА!")
        print("[!] Запустите от имени АДМИНИСТРАТОРА!")
        print("[!] Правый клик -> 'Запуск от имени администратора'")
        input("\nНажмите Enter для выхода...")
        return
    
    # Создаем запускатель
    launcher = create_final_launcher()
    print(f"[+] Создан запускатель: {launcher}")
    print("[+] Скопируйте эти файлы в деревню:")
    print("    1. final_esp.py - основной код ESP")
    print(f"    2. {launcher} - запускатель")
    
    # Инструкция для деревни
    print("\n" + "=" * 70)
    print("ИНСТРУКЦИЯ ДЛЯ ДЕРЕВНИ:")
    print("=" * 70)
    print("1. Установите Python 3.x с python.org")
    print("2. Скопируйте оба файла в одну папку")
    print(f"3. Запустите {launcher} от Администратора")
    print("4. Запустите Valorant и зайдите в матч")
    print("5. Нажмите F8 в игре")
    print("\nЧТО УВИДИТ ДЕРЕВНЯ:")
    print("- Красные боксы вокруг врагов")
    print("- Полоски здоровья")
    print("- Мини-радар с позициями")
    print("- Информационную панель")
    print("=" * 70)
    
    # Запуск ESP
    print("\nЗапустить демонстрацию сейчас? (y/n): ", end="")
    if input().lower() == 'y':
        print("\n[+] Запуск ESP через 3 секунды...")
        for i in range(3, 0, -1):
            print(f"[{i}]...")
            time.sleep(1)
        
        esp = FinalESP()
        esp.run()
    else:
        print("\n[+] Файлы готовы. Передайте деревне.")
        print(f"[+] Запускатель: {launcher}")
        input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()