from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Calculator:
    def __init__(self, ui):
        self.ui = ui
        self.setup_calculator()
        
    def setup_calculator(self):
        """Настройка калькулятора"""
        # Настройка шрифта для дисплея
        font = QFont()
        font.setPointSize(18)
        self.ui.display.setFont(font)
        
        # Подключение кнопок
        self.connect_buttons()
        
        # Переменные для вычислений
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.result_displayed = False

    def connect_buttons(self):
        """Подключение всех кнопок к обработчикам"""
        # Цифровые кнопки
        self.ui.btn_0.clicked.connect(lambda: self.input_digit('0'))
        self.ui.btn_1.clicked.connect(lambda: self.input_digit('1'))
        self.ui.btn_2.clicked.connect(lambda: self.input_digit('2'))
        self.ui.btn_3.clicked.connect(lambda: self.input_digit('3'))
        self.ui.btn_4.clicked.connect(lambda: self.input_digit('4'))
        self.ui.btn_5.clicked.connect(lambda: self.input_digit('5'))
        self.ui.btn_6.clicked.connect(lambda: self.input_digit('6'))
        self.ui.btn_7.clicked.connect(lambda: self.input_digit('7'))
        self.ui.btn_8.clicked.connect(lambda: self.input_digit('8'))
        self.ui.btn_9.clicked.connect(lambda: self.input_digit('9'))
        
        # Операторы
        self.ui.btn_add.clicked.connect(lambda: self.input_operator('+'))
        self.ui.btn_subtract.clicked.connect(lambda: self.input_operator('-'))
        self.ui.btn_multiply.clicked.connect(lambda: self.input_operator('×'))
        self.ui.btn_divide.clicked.connect(lambda: self.input_operator('/'))
        
        # Специальные кнопки
        self.ui.btn_clear.clicked.connect(self.clear)
        self.ui.btn_equals.clicked.connect(self.calculate)
        self.ui.btn_decimal.clicked.connect(self.input_decimal)
        self.ui.btn_sign.clicked.connect(self.toggle_sign)
        self.ui.btn_percent.clicked.connect(self.percentage)

    def input_digit(self, digit):
        if self.result_displayed or self.current_input == "0":
            self.current_input = digit
            self.result_displayed = False
        else:
            self.current_input += digit
        
        self.ui.display.setText(self.current_input)

    def input_decimal(self):
        if self.result_displayed:
            self.current_input = "0."
            self.result_displayed = False
        elif '.' not in self.current_input:
            self.current_input += '.'
        
        self.ui.display.setText(self.current_input)

    def input_operator(self, op):
        if self.current_input and self.previous_input and self.operator:
            self.calculate()
        
        if self.current_input:
            self.previous_input = self.current_input
            self.current_input = ""
        
        self.operator = op
        self.result_displayed = False

    def calculate(self):
        if not self.previous_input or not self.current_input or not self.operator:
            return
        
        try:
            prev = float(self.previous_input)
            curr = float(self.current_input)
            
            if self.operator == '+':
                result = prev + curr
            elif self.operator == '-':
                result = prev - curr
            elif self.operator == '×':
                result = prev * curr
            elif self.operator == '/':
                if curr == 0:
                    self.ui.display.setText("Ошибка")
                    self.clear()
                    return
                result = prev / curr
            
            # Форматирование результата
            if result.is_integer():
                self.current_input = str(int(result))
            else:
                self.current_input = str(round(result, 10)).rstrip('0').rstrip('.')
            
            self.ui.display.setText(self.current_input)
            self.previous_input = ""
            self.operator = ""
            self.result_displayed = True
            
        except (ValueError, ZeroDivisionError):
            self.ui.display.setText("Ошибка")
            self.clear()

    def clear(self):
        self.current_input = "0"
        self.previous_input = ""
        self.operator = ""
        self.result_displayed = False
        self.ui.display.setText("0")

    def toggle_sign(self):
        if self.current_input and self.current_input != "0":
            if self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.ui.display.setText(self.current_input)

    def percentage(self):
        if self.current_input:
            try:
                value = float(self.current_input) / 100
                if value.is_integer():
                    self.current_input = str(int(value))
                else:
                    self.current_input = str(value)
                self.ui.display.setText(self.current_input)
            except ValueError:
                self.ui.display.setText("Ошибка")
                self.clear()

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        key = event.key()
        
        if key >= Qt.Key.Key_0 and key <= Qt.Key.Key_9:
            self.input_digit(chr(key))
        elif key == Qt.Key.Key_Plus:
            self.input_operator('+')
        elif key == Qt.Key.Key_Minus:
            self.input_operator('-')
        elif key in [Qt.Key.Key_Asterisk, Qt.Key.Key_multiply]:
            self.input_operator('×')
        elif key in [Qt.Key.Key_Slash, Qt.Key.Key_division]:
            self.input_operator('/')
        elif key in [Qt.Key.Key_Return, Qt.Key.Key_Equal]:
            self.calculate()
        elif key == Qt.Key.Key_Period:
            self.input_decimal()
        elif key == Qt.Key.Key_Escape:
            self.clear()
        elif key == Qt.Key.Key_Backspace:
            if len(self.current_input) > 1:
                self.current_input = self.current_input[:-1]
                self.ui.display.setText(self.current_input)
            else:
                self.current_input = "0"
                self.ui.display.setText("0")