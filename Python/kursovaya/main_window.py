from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from warehouse import Warehouse

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.warehouse = Warehouse()
        self.setup_ui()
        self.warehouse.load_from_file()
        self.update_product_list()
    
    def setup_ui(self):
        self.setWindowTitle("Складской учет")
        self.setGeometry(100, 100, 800, 500)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # Форма добавления товара
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.price_input = QLineEdit()
        self.quantity_input = QLineEdit()
        
        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Цена:", self.price_input)
        form_layout.addRow("Количество:", self.quantity_input)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить товар")
        self.add_btn.clicked.connect(self.add_product)
        
        self.update_btn = QPushButton("Изменить количество")
        self.update_btn.clicked.connect(self.update_quantity)
        
        self.delete_btn = QPushButton("Удалить товар")
        self.delete_btn.clicked.connect(self.delete_product)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        
        # Список товаров
        self.product_list = QListWidget()
        
        # Добавляем все в основной layout
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("Список товаров:"))
        layout.addWidget(self.product_list)
        
        central_widget.setLayout(layout)
    
    def add_product(self):
        name = self.name_input.text()
        price = self.price_input.text()
        quantity = self.quantity_input.text()
        
        if name and price and quantity:
            try:
                self.warehouse.add_product(name, float(price), int(quantity))
                self.clear_inputs()
                self.update_product_list()
                self.warehouse.save_to_file()
                QMessageBox.information(self, "Успех", "Товар добавлен!")
            except:
                QMessageBox.warning(self, "Ошибка", "Проверьте данные!")
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
    
    def update_quantity(self):
        selected = self.product_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите товар!")
            return
        
        # Получаем ID из текста (первое число в строке)
        product_id = int(selected.text().split(":")[0])
        
        new_quantity, ok = QInputDialog.getInt(
            self, "Изменение количества", 
            "Введите новое количество:", 
            value=10, min=0, max=10000
        )
        
        if ok:
            if self.warehouse.update_quantity(product_id, new_quantity):
                self.update_product_list()
                self.warehouse.save_to_file()
                QMessageBox.information(self, "Успех", "Количество обновлено!")
    
    def delete_product(self):
        selected = self.product_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите товар!")
            return
        
        product_id = int(selected.text().split(":")[0])
        
        reply = QMessageBox.question(
            self, "Подтверждение", 
            "Удалить этот товар?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.warehouse.remove_product(product_id):
                self.update_product_list()
                self.warehouse.save_to_file()
                QMessageBox.information(self, "Успех", "Товар удален!")
    
    def update_product_list(self):
        self.product_list.clear()
        for product in self.warehouse.get_all_products():
            self.product_list.addItem(
                f"{product.product_id}: {product.name} - {product.price} руб. ({product.quantity} шт.)"
            )
    
    def clear_inputs(self):
        self.name_input.clear()
        self.price_input.clear()
        self.quantity_input.clear()
    
    def closeEvent(self, event):
        self.warehouse.save_to_file()
        event.accept()