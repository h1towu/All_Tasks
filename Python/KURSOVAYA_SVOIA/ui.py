import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QMessageBox,
    QGroupBox, QFormLayout, QSpinBox, QHeaderView
)
from PyQt6.QtCore import Qt
from logic import WarehouseSystem

class WarehouseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.system = WarehouseSystem()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Складская система")
        self.setGeometry(100, 100, 900, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        form_group = QGroupBox("Добавить товар")
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название товара")
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(9999)
        self.quantity_input.setValue(1)
        
        self.price_input = QSpinBox()
        self.price_input.setMinimum(1)
        self.price_input.setMaximum(999999)
        self.price_input.setValue(100)
        self.price_input.setSuffix(" руб.")
        
        form_layout.addRow("Название:", self.name_input)
        form_layout.addRow("Количество:", self.quantity_input)
        form_layout.addRow("Цена:", self.price_input)
        
        self.add_button = QPushButton("Добавить товар")
        self.add_button.clicked.connect(self.add_item)
        form_layout.addRow(self.add_button)
        
        form_group.setLayout(form_layout)
        left_layout.addWidget(form_group)
        
        delete_group = QGroupBox("Удалить товар")
        delete_layout = QVBoxLayout()
        
        self.delete_name_input = QLineEdit()
        self.delete_name_input.setPlaceholderText("Введите название товара для удаления")
        delete_layout.addWidget(self.delete_name_input)
        
        self.delete_button = QPushButton("Удалить товар")
        self.delete_button.clicked.connect(self.remove_item)
        delete_layout.addWidget(self.delete_button)
        
        delete_group.setLayout(delete_layout)
        left_layout.addWidget(delete_group)
        
        stats_group = QGroupBox("Статистика")
        stats_layout = QVBoxLayout()
        
        self.stats_label = QLabel("Всего товаров: 0")
        stats_layout.addWidget(self.stats_label)
        
        self.total_value_label = QLabel("Общая стоимость: 0 руб.")
        stats_layout.addWidget(self.total_value_label)
        
        self.file_info_label = QLabel("Данные сохраняются автоматически")
        self.file_info_label.setStyleSheet("color: blue; font-size: 10px;")
        stats_layout.addWidget(self.file_info_label)
        
        stats_group.setLayout(stats_layout)
        left_layout.addWidget(stats_group)
        
        left_layout.addStretch()
        left_panel.setLayout(left_layout)
        left_panel.setFixedWidth(350)
        main_layout.addWidget(left_panel)
        
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        right_layout.addWidget(QLabel("<b>Список товаров:</b>"))
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(3)
        self.items_table.setHorizontalHeaderLabels(["Название", "Количество", "Цена"])
        self.items_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.items_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.items_table.setAlternatingRowColors(True)
        right_layout.addWidget(self.items_table)
        
        right_panel.setLayout(right_layout)
        main_layout.addWidget(right_panel)
        
        self.update_items_list()
        
    def add_item(self):
        name = self.name_input.text().strip()
        quantity = self.quantity_input.value()
        price = self.price_input.value()
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название товара!")
            return
            
        try:
            result = self.system.add_item(name, quantity, price)
            QMessageBox.information(self, "Успех", result)
            self.update_items_list()
            self.clear_inputs()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить товар: {str(e)}")
            
    def remove_item(self):
        name = self.delete_name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название товара!")
            return
            
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Вы уверены, что хотите удалить товар '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            result = self.system.remove_item(name)
            QMessageBox.information(self, "Результат", result)
            self.update_items_list()
            self.delete_name_input.clear()
            
    def update_items_list(self):
        items = self.system.get_all_items()
        self.items_table.setRowCount(len(items))
        
        for row, item in enumerate(items):
            name_item = QTableWidgetItem(item.name)
            self.items_table.setItem(row, 0, name_item)
            
            quantity_item = QTableWidgetItem(str(item.quantity))
            quantity_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.items_table.setItem(row, 1, quantity_item)
            
            price_item = QTableWidgetItem(f"{item.price} руб.")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.items_table.setItem(row, 2, price_item)
        
        total_items = self.system.get_items_count()
        self.stats_label.setText(f"Всего товаров: {total_items}")
        
        total_value = self.system.get_total_value()
        self.total_value_label.setText(f"Общая стоимость: {total_value} руб.")
        
    def clear_inputs(self):
        self.name_input.clear()
        self.quantity_input.setValue(1)
        self.price_input.setValue(100)
        
    def closeEvent(self, event):
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = WarehouseApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()