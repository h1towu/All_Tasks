// main.cpp - демонстрация работы контейнера, ломаной и стека
#include "polyline.h"
#include "stack.h"  // добавляем стек
#include "point.h"
#include "point_container.h"
#include "stack.h"
#include <iostream>

using namespace std;

void demonstrateStack() {
    cout << "\n=== ДЕМОНСТРАЦИЯ СТЕКА ТОЧЕК ===" << endl;
    
    PointStack stack;
    
    cout << "\n--- Добавление точек в стек ---" << endl;
    stack.push(Point(1, 1));
    stack.push(Point(2, 2));
    stack.push(Point(3, 3));
    stack.push(4, 4);
    stack.push(5, 5);
    
    stack.print();
    
    cout << "\n--- Верхняя точка стека ---" << endl;
    Point top = stack.peek();
    cout << "Верхняя точка: ";
    top.print();
    cout << endl;
    
    cout << "\n--- Извлечение точек из стека ---" << endl;
    while (!stack.isEmpty()) {
        Point p = stack.pop();
        cout << "Извлечена точка: ";
        p.print();
        cout << endl;
        stack.print();
    }
}

void demonstratePolyline() {
    cout << "\n=== ДЕМОНСТРАЦИЯ ЛОМАНОЙ ===" << endl;
    
    Polyline line("Основная ломаная");
    
    cout << "--- Добавление точек ---" << endl;
    line.addPoint(Point(0, 0));
    line.addPoint(Point(3, 4));
    line.addPoint(Point(6, 8));
    line.addPoint(Point(10, 10));
    
    line.print();
    
    cout << "--- Удаление точки ---" << endl;
    line.removePoint(1);
    line.print();
}

void demonstrateContainer() {
    cout << "\n=== ДЕМОНСТРАЦИЯ КОНТЕЙНЕРА ===" << endl;
    
    PointContainer container;
    container.addPoint(Point(1, 1));
    container.addPoint(Point(2, 2));
    container.addPoint(Point(3, 3));
    
    cout << "Количество точек в контейнере: " << container.getSize() << endl;
    
    // Поиск точки
    Point searchPoint(2, 2);
    int foundIndex = container.findPoint(searchPoint);
    if (foundIndex != -1) {
        cout << "Точка найдена на позиции: " << foundIndex << endl;
    }
}

void demonstrateStackWithPolyline() {
    cout << "\n=== ИСПОЛЬЗОВАНИЕ СТЕКА С ЛОМАНОЙ ===" << endl;
    
    // Создаем ломаную и стек
    Polyline line("Ломаная из стека");
    PointStack stack;
    
    // Заполняем стек точками
    cout << "--- Заполняем стек ---" << endl;
    stack.push(Point(0, 0));
    stack.push(Point(2, 3));
    stack.push(Point(4, 1));
    stack.push(Point(6, 5));
    
    // Переносим точки из стека в ломаную
    cout << "\n--- Перенос точек из стека в ломаную ---" << endl;
    while (!stack.isEmpty()) {
        Point p = stack.pop();
        line.addPoint(p);
    }
    
    line.print();
}

int main() {
    cout << "=== ДЕМОНСТРАЦИЯ КОНТЕЙНЕРА, ЛОМАНОЙ И СТЕКА ===" << endl;
    
    demonstrateContainer();
    demonstratePolyline();
    demonstrateStack();
    demonstrateStackWithPolyline();
    
    cout << "\nПрограмма завершена!" << endl;
    return 0;
}
/*
# Компилируем все модули (добавляем стек)
g++ -c point.cpp -o point.o
g++ -c point_container.cpp -o point_container.o
g++ -c polyline.cpp -o polyline.o
g++ -c stack.cpp -o stack.o          # новый файл
g++ -c main.cpp -o main.o

# Связываем все вместе
g++ point.o point_container.o polyline.o stack.o main.o -o graphics_program

# Запускаем
./graphics_program
*/