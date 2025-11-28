# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'calculator.ui'
################################################################################

from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(300, 400)
        MainWindow.setMinimumSize(QSize(300, 400))
        MainWindow.setMaximumSize(QSize(300, 400))
        MainWindow.setStyleSheet(u"background-color: #2b2b2b;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.display = QLineEdit(self.centralwidget)
        self.display.setObjectName(u"display")
        self.display.setMinimumSize(QSize(0, 70))
        self.display.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #4a90e2;\n"
"    border-radius: 15px;\n"
"    padding: 0 15px;\n"
"    background-color: #1e1e1e;\n"
"    color: #ffffff;\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"}")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)

        self.verticalLayout.addWidget(self.display)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(10)
        self.btn_7 = QPushButton(self.centralwidget)
        self.btn_7.setObjectName(u"btn_7")
        self.btn_7.setMinimumSize(QSize(60, 60))
        self.btn_7.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_7, 1, 0, 1, 1)

        self.btn_8 = QPushButton(self.centralwidget)
        self.btn_8.setObjectName(u"btn_8")
        self.btn_8.setMinimumSize(QSize(60, 60))
        self.btn_8.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_8, 1, 1, 1, 1)

        self.btn_9 = QPushButton(self.centralwidget)
        self.btn_9.setObjectName(u"btn_9")
        self.btn_9.setMinimumSize(QSize(60, 60))
        self.btn_9.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_9, 1, 2, 1, 1)

        self.btn_divide = QPushButton(self.centralwidget)
        self.btn_divide.setObjectName(u"btn_divide")
        self.btn_divide.setMinimumSize(QSize(60, 60))
        self.btn_divide.setStyleSheet(u"QPushButton {\n"
"    background-color: #ff9500;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 30px;\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #ffaa33;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #cc7700;\n"
"}")

        self.gridLayout.addWidget(self.btn_divide, 0, 3, 1, 1)

        self.btn_4 = QPushButton(self.centralwidget)
        self.btn_4.setObjectName(u"btn_4")
        self.btn_4.setMinimumSize(QSize(60, 60))
        self.btn_4.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_4, 2, 0, 1, 1)

        self.btn_5 = QPushButton(self.centralwidget)
        self.btn_5.setObjectName(u"btn_5")
        self.btn_5.setMinimumSize(QSize(60, 60))
        self.btn_5.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_5, 2, 1, 1, 1)

        self.btn_6 = QPushButton(self.centralwidget)
        self.btn_6.setObjectName(u"btn_6")
        self.btn_6.setMinimumSize(QSize(60, 60))
        self.btn_6.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_6, 2, 2, 1, 1)

        self.btn_multiply = QPushButton(self.centralwidget)
        self.btn_multiply.setObjectName(u"btn_multiply")
        self.btn_multiply.setMinimumSize(QSize(60, 60))
        self.btn_multiply.setStyleSheet(u"QPushButton {\n"
"    background-color: #ff9500;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 30px;\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #ffaa33;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #cc7700;\n"
"}")

        self.gridLayout.addWidget(self.btn_multiply, 1, 3, 1, 1)

        self.btn_1 = QPushButton(self.centralwidget)
        self.btn_1.setObjectName(u"btn_1")
        self.btn_1.setMinimumSize(QSize(60, 60))
        self.btn_1.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_1, 3, 0, 1, 1)

        self.btn_2 = QPushButton(self.centralwidget)
        self.btn_2.setObjectName(u"btn_2")
        self.btn_2.setMinimumSize(QSize(60, 60))
        self.btn_2.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_2, 3, 1, 1, 1)

        self.btn_3 = QPushButton(self.centralwidget)
        self.btn_3.setObjectName(u"btn_3")
        self.btn_3.setMinimumSize(QSize(60, 60))
        self.btn_3.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_3, 3, 2, 1, 1)

        self.btn_subtract = QPushButton(self.centralwidget)
        self.btn_subtract.setObjectName(u"btn_subtract")
        self.btn_subtract.setMinimumSize(QSize(60, 60))
        self.btn_subtract.setStyleSheet(u"QPushButton {\n"
"    background-color: #ff9500;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 30px;\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #ffaa33;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #cc7700;\n"
"}")

        self.gridLayout.addWidget(self.btn_subtract, 2, 3, 1, 1)

        self.btn_0 = QPushButton(self.centralwidget)
        self.btn_0.setObjectName(u"btn_0")
        self.btn_0.setMinimumSize(QSize(130, 60))
        self.btn_0.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_0, 4, 0, 1, 2)

        self.btn_decimal = QPushButton(self.centralwidget)
        self.btn_decimal.setObjectName(u"btn_decimal")
        self.btn_decimal.setMinimumSize(QSize(60, 60))
        self.btn_decimal.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2d2d;\n"
"    border: 2px solid #3d3d3d;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    color: #ffffff;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3d3d3d;\n"
"    border-color: #4d4d4d;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4d4d4d;\n"
"    border-color: #5d5d5d;\n"
"}")

        self.gridLayout.addWidget(self.btn_decimal, 4, 2, 1, 1)

        self.btn_equals = QPushButton(self.centralwidget)
        self.btn_equals.setObjectName(u"btn_equals")
        self.btn_equals.setMinimumSize(QSize(60, 60))
        self.btn_equals.setStyleSheet(u"QPushButton {\n"
"    background-color: #ff9500;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 30px;\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #ffaa33;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #cc7700;\n"
"}")

        self.gridLayout.addWidget(self.btn_equals, 4, 3, 1, 1)

        self.btn_add = QPushButton(self.centralwidget)
        self.btn_add.setObjectName(u"btn_add")
        self.btn_add.setMinimumSize(QSize(60, 60))
        self.btn_add.setStyleSheet(u"QPushButton {\n"
"    background-color: #ff9500;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 30px;\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #ffaa33;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #cc7700;\n"
"}")

        self.gridLayout.addWidget(self.btn_add, 3, 3, 1, 1)

        self.btn_clear = QPushButton(self.centralwidget)
        self.btn_clear.setObjectName(u"btn_clear")
        self.btn_clear.setMinimumSize(QSize(60, 60))
        self.btn_clear.setStyleSheet(u"QPushButton {\n"
"    background-color: #a6a6a6;\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #b8b8b8;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #8c8c8c;\n"
"}")

        self.gridLayout.addWidget(self.btn_clear, 0, 0, 1, 1)

        self.btn_sign = QPushButton(self.centralwidget)
        self.btn_sign.setObjectName(u"btn_sign")
        self.btn_sign.setMinimumSize(QSize(60, 60))
        self.btn_sign.setStyleSheet(u"QPushButton {\n"
"    background-color: #a6a6a6;\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #b8b8b8;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #8c8c8c;\n"
"}")

        self.gridLayout.addWidget(self.btn_sign, 0, 1, 1, 1)

        self.btn_percent = QPushButton(self.centralwidget)
        self.btn_percent.setObjectName(u"btn_percent")
        self.btn_percent.setMinimumSize(QSize(60, 60))
        self.btn_percent.setStyleSheet(u"QPushButton {\n"
"    background-color: #a6a6a6;\n"
"    color: #000000;\n"
"    border: none;\n"
"    border-radius: 30px;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #b8b8b8;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #8c8c8c;\n"
"}")

        self.gridLayout.addWidget(self.btn_percent, 0, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043b\u044c\u043a\u0443\u043b\u044f\u0442\u043e\u0440", None))
        self.display.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.btn_7.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.btn_8.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.btn_9.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.btn_divide.setText(QCoreApplication.translate("MainWindow", u"/", None))
        self.btn_4.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.btn_5.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.btn_6.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.btn_multiply.setText(QCoreApplication.translate("MainWindow", u"\u00d7", None))
        self.btn_1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.btn_2.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.btn_3.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.btn_subtract.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.btn_0.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.btn_decimal.setText(QCoreApplication.translate("MainWindow", u".", None))
        self.btn_equals.setText(QCoreApplication.translate("MainWindow", u"=", None))
        self.btn_add.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.btn_clear.setText(QCoreApplication.translate("MainWindow", u"C", None))
        self.btn_sign.setText(QCoreApplication.translate("MainWindow", u"\u00b1", None))
        self.btn_percent.setText(QCoreApplication.translate("MainWindow", u"%", None))
    # retranslateUi