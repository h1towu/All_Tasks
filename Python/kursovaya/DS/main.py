from ui import WarehouseUI
from PyQt6.QtWidgets import QApplication

class WarehouseItem:
    """Класс для товара на складе"""
    def __init__(self, item_id, name, quantity, price):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price
    
    def get_total_value(self):
        """Получить общую стоимость товара"""
        return float(self.quantity) * float(self.price)
    
    def to_list(self):
        """Преобразовать в список для отображения"""
        return [self.item_id, self.name, self.quantity, self.price]

class WarehouseSystem:
    """Основной класс системы складского учета"""
    def __init__(self, filename='warehouse.txt'):
        self.filename = filename
        self.items = {}
        self.next_id = 1
        self.load_data()
    
    def load_data(self):
        """Загрузить данные из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 4:
                            item_id = int(parts[0])
                            name = parts[1]
                            quantity = float(parts[2])
                            price = float(parts[3])
                            
                            self.items[item_id] = WarehouseItem(item_id, name, quantity, price)
                            if item_id >= self.next_id:
                                self.next_id = item_id + 1
        except FileNotFoundError:
            self.save_data()
    
    def save_data(self):
        """Сохранить данные в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                for item in self.items.values():
                    f.write(f"{item.item_id},{item.name},{item.quantity},{item.price}\n")
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False
    
    def add_item(self, name, quantity, price):
        """Добавить новый товар"""
        try:
            quantity = float(quantity)
            price = float(price)
            
            if quantity <= 0 or price <= 0:
                return False, "Количество и цена должны быть положительными числами"
            
            item = WarehouseItem(self.next_id, name, quantity, price)
            self.items[self.next_id] = item
            self.next_id += 1
            self.save_data()
            return True, "Товар успешно добавлен"
        except ValueError:
            return False, "Некорректный формат данных"
    
    def update_item(self, item_id, name, quantity, price):
        """Обновить существующий товар"""
        if item_id not in self.items:
            return False, "Товар не найден"
        
        try:
            quantity = float(quantity)
            price = float(price)
            
            if quantity <= 0 or price <= 0:
                return False, "Количество и цена должны быть положительными числами"
            
            self.items[item_id].name = name
            self.items[item_id].quantity = quantity
            self.items[item_id].price = price
            self.save_data()
            return True, "Товар успешно обновлен"
        except ValueError:
            return False, "Некорректный формат данных"
    
    def remove_item(self, item_id):
        """Удалить товар"""
        if item_id in self.items:
            del self.items[item_id]
            self.save_data()
            return True, "Товар успешно удален"
        return False, "Товар не найден"
    
    def get_all_items(self):
        """Получить все товары"""
        return [item.to_list() for item in self.items.values()]
    
    def search_item(self, keyword):
        """Найти товары по ключевому слову"""
        results = []
        keyword = keyword.lower()
        
        for item in self.items.values():
            if keyword in item.name.lower():
                results.append(item.to_list())
        
        return results
    
    def get_total_info(self):
        """Получить общую информацию о складе"""
        total_items = len(self.items)
        total_value = sum(item.get_total_value() for item in self.items.values())
        return total_items, total_value

class WarehouseApp:
    """Класс приложения"""
    def __init__(self):
        self.warehouse = WarehouseSystem()
        self.ui = WarehouseUI()
        self.setup_connections()
    
    def setup_connections(self):
        """Настроить соединения сигналов и слотов"""
        self.ui.add_button.clicked.connect(self.add_item)
        self.ui.update_button.clicked.connect(self.update_item)
        self.ui.remove_button.clicked.connect(self.remove_item)
        self.ui.search_button.clicked.connect(self.search_items)
        self.ui.show_all_button.clicked.connect(self.show_all_items)
        self.ui.table.itemSelectionChanged.connect(self.on_item_selected)
        
        # Показать все товары при запуске
        self.show_all_items()
    
    def add_item(self):
        """Добавить товар"""
        name, quantity, price = self.ui.get_form_data()
        
        if not name or not quantity or not price:
            self.ui.show_error("Заполните все поля")
            return
        
        success, message = self.warehouse.add_item(name, quantity, price)
        
        if success:
            self.ui.show_message("Успех", message)
            self.ui.clear_form()
            self.show_all_items()
        else:
            self.ui.show_error(message)
    
    def update_item(self):
        """Обновить товар"""
        item_id = self.ui.get_current_item_id()
        
        if item_id is None:
            self.ui.show_error("Выберите товар для обновления")
            return
        
        name, quantity, price = self.ui.get_form_data()
        
        if not name or not quantity or not price:
            self.ui.show_error("Заполните все поля")
            return
        
        success, message = self.warehouse.update_item(item_id, name, quantity, price)
        
        if success:
            self.ui.show_message("Успех", message)
            self.ui.clear_form()
            self.show_all_items()
        else:
            self.ui.show_error(message)
    
    def remove_item(self):
        """Удалить товар"""
        item_id = self.ui.get_current_item_id()
        
        if item_id is None:
            self.ui.show_error("Выберите товар для удаления")
            return
        
        success, message = self.warehouse.remove_item(item_id)
        
        if success:
            self.ui.show_message("Успех", message)
            self.show_all_items()
        else:
            self.ui.show_error(message)
    
    def search_items(self):
        """Поиск товаров"""
        keyword = self.ui.name_input.text().strip()
        
        if not keyword:
            self.ui.show_error("Введите название для поиска")
            return
        
        results = self.warehouse.search_item(keyword)
        
        if results:
            self.ui.update_table(results)
            total_items = len(results)
            total_value = sum(float(item[2]) * float(item[3]) for item in results)
            self.ui.update_total_info(total_items, total_value)
        else:
            self.ui.update_table([])
            self.ui.update_total_info(0, 0)
            self.ui.show_message("Результаты", "Товары не найдены")
    
    def show_all_items(self):
        """Показать все товары"""
        items = self.warehouse.get_all_items()
        self.ui.update_table(items)
        
        total_items, total_value = self.warehouse.get_total_info()
        self.ui.update_total_info(total_items, total_value)
    
    def on_item_selected(self):
        """При выборе товара в таблице"""
        item_id = self.ui.get_current_item_id()
        
        if item_id is not None and item_id in self.warehouse.items:
            item = self.warehouse.items[item_id]
            self.ui.name_input.setText(item.name)
            self.ui.quantity_input.setText(str(item.quantity))
            self.ui.price_input.setText(str(item.price))
    
    def run(self):
        """Запустить приложение"""
        self.ui.show()

def main():
    app = QApplication([])
    warehouse_app = WarehouseApp()
    warehouse_app.run()
    app.exec()

if __name__ == "__main__":
    main()