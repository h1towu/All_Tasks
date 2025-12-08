import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QHBoxLayout
)
from main import Warehouse

class WarehouseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Складской учёт")
        self.setGeometry(200, 200, 500, 400)

        self.warehouse = Warehouse()

        layout = QVBoxLayout()

        # Список товаров
        self.list_widget = QListWidget()
        layout.addWidget(QLabel("Товары на складе:"))
        layout.addWidget(self.list_widget)

        # Поля ввода
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название товара")
        layout.addWidget(self.name_input)

        self.qty_input = QLineEdit()
        self.qty_input.setPlaceholderText("Количество")
        layout.addWidget(self.qty_input)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Цена за единицу")
        layout.addWidget(self.price_input)

        # Кнопки
        add_btn = QPushButton("Добавить товар")
        add_btn.clicked.connect(self.add_item)
        layout.addWidget(add_btn)

        # Кнопки увеличить/уменьшить
        h_layout = QHBoxLayout()
        inc_btn = QPushButton("Увеличить количество")
        inc_btn.clicked.connect(self.increase_item)
        h_layout.addWidget(inc_btn)

        dec_btn = QPushButton("Уменьшить количество")
        dec_btn.clicked.connect(self.decrease_item)
        h_layout.addWidget(dec_btn)

        layout.addLayout(h_layout)

        # Общая стоимость
        self.total_label = QLabel("Общая стоимость: 0")
        layout.addWidget(self.total_label)

        self.setLayout(layout)
        self.refresh_list()

    def refresh_list(self):
        self.list_widget.clear()
        items = self.warehouse.show_items()
        for name, data in items.items():
            self.list_widget.addItem(f"{name} - {data['qty']} шт. по {data['price']} руб.")
        self.total_label.setText(f"Общая стоимость: {self.warehouse.total_value()} руб.")

    def add_item(self):
        name = self.name_input.text()
        try:
            qty = int(self.qty_input.text())
            price = float(self.price_input.text())
        except:
            qty, price = 0, 0
        self.warehouse.add_item(name, qty, price)
        self.refresh_list()

    def increase_item(self):
        name = self.name_input.text()
        try:
            qty = int(self.qty_input.text())
        except:
            qty = 1
        self.warehouse.increase_item(name, qty)
        self.refresh_list()

    def decrease_item(self):
        name = self.name_input.text()
        try:
            qty = int(self.qty_input.text())
        except:
            qty = 1
        self.warehouse.decrease_item(name, qty)
        self.refresh_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WarehouseApp()
    window.show()
    sys.exit(app.exec())
