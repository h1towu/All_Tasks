from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt

class WarehouseUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Складской учет")
        self.setGeometry(100, 100, 800, 600)
        
        # Основной виджет
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Основной layout
        main_layout = QVBoxLayout(main_widget)
        
        # Заголовок
        title_label = QLabel("Система складского учета")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(title_label)
        
        # Форма для добавления/обновления товаров
        form_layout = QVBoxLayout()
        
        # Название товара
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название товара:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название товара")
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)
        
        # Количество
        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel("Количество:"))
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Введите количество")
        quantity_layout.addWidget(self.quantity_input)
        form_layout.addLayout(quantity_layout)
        
        # Цена
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("Цена:"))
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Введите цену")
        price_layout.addWidget(self.price_input)
        form_layout.addLayout(price_layout)
        
        # Кнопки действий
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Добавить товар")
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        buttons_layout.addWidget(self.add_button)
        
        self.update_button = QPushButton("Обновить товар")
        self.update_button.setStyleSheet("background-color: #2196F3; color: white; padding: 5px;")
        buttons_layout.addWidget(self.update_button)
        
        self.remove_button = QPushButton("Удалить товар")
        self.remove_button.setStyleSheet("background-color: #f44336; color: white; padding: 5px;")
        buttons_layout.addWidget(self.remove_button)
        
        self.search_button = QPushButton("Поиск")
        self.search_button.setStyleSheet("background-color: #FF9800; color: white; padding: 5px;")
        buttons_layout.addWidget(self.search_button)
        
        self.show_all_button = QPushButton("Показать все")
        self.show_all_button.setStyleSheet("background-color: #9C27B0; color: white; padding: 5px;")
        buttons_layout.addWidget(self.show_all_button)
        
        form_layout.addLayout(buttons_layout)
        main_layout.addLayout(form_layout)
        
        # Таблица для отображения товаров
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Количество", "Цена", "Стоимость"])
        main_layout.addWidget(self.table)
        
        # Информация о складе
        self.total_label = QLabel("Всего товаров: 0 | Общая стоимость: 0")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_label.setStyleSheet("font-size: 14px; padding: 5px; background-color: #E3F2FD;")
        main_layout.addWidget(self.total_label)
        
        # Сообщение об ошибках
        self.error_label = QLabel("")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet("color: red; padding: 5px;")
        main_layout.addWidget(self.error_label)
    
    def show_message(self, title, message):
        """Показать сообщение"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()
    
    def clear_form(self):
        """Очистить форму ввода"""
        self.name_input.clear()
        self.quantity_input.clear()
        self.price_input.clear()
        self.error_label.setText("")
    
    def show_error(self, message):
        """Показать ошибку"""
        self.error_label.setText(message)
    
    def update_table(self, items):
        """Обновить таблицу с товарами"""
        self.table.setRowCount(len(items))
        
        for row, item in enumerate(items):
            item_id, name, quantity, price = item
            total_value = float(quantity) * float(price)
            
            self.table.setItem(row, 0, QTableWidgetItem(str(item_id)))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(str(quantity)))
            self.table.setItem(row, 3, QTableWidgetItem(str(price)))
            self.table.setItem(row, 4, QTableWidgetItem(f"{total_value:.2f}"))
    
    def update_total_info(self, total_items, total_value):
        """Обновить информацию о складе"""
        self.total_label.setText(f"Всего товаров: {total_items} | Общая стоимость: {total_value:.2f}")
    
    def get_current_item_id(self):
        """Получить ID выбранного товара"""
        selected_items = self.table.selectedItems()
        if selected_items:
            return int(self.table.item(selected_items[0].row(), 0).text())
        return None
    
    def get_form_data(self):
        """Получить данные из формы"""
        name = self.name_input.text().strip()
        quantity = self.quantity_input.text().strip()
        price = self.price_input.text().strip()
        return name, quantity, price