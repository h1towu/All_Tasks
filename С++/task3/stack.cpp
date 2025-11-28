// stack.cpp - реализация стека точек
#include "stack.h"
#include <iostream>

using namespace std;

PointStack::PointStack() {
    cout << "Создан стек точек" << endl;
}

void PointStack::push(const Point& point) {
    container.addPoint(point);
    cout << "Точка добавлена в стек. Размер стека: " << container.getSize() << endl;
}

void PointStack::push(double x, double y) {
    Point point(x, y);
    container.addPoint(point);
    cout << "Точка (" << x << ", " << y << ") добавлена в стек. Размер: " << container.getSize() << endl;
}

Point PointStack::pop() {
    if (container.isEmpty()) {
        cout << "Ошибка: стек пуст! Возвращена точка (0,0)" << endl;
        return Point(0, 0);
    }
    
    int lastIndex = container.getSize() - 1;
    Point topPoint = container.getPoint(lastIndex);
    container.removePoint(lastIndex);
    
    cout << "Точка извлечена из стека. Осталось: " << container.getSize() << endl;
    return topPoint;
}

Point PointStack::peek() const {
    if (container.isEmpty()) {
        cout << "Ошибка: стек пуст! Возвращена точка (0,0)" << endl;
        return Point(0, 0);
    }
    
    return container.getPoint(container.getSize() - 1);
}

bool PointStack::isEmpty() const {
    return container.isEmpty();
}

int PointStack::getSize() const {
    return container.getSize();
}

void PointStack::clear() {
    container.clear();
    cout << "Стек очищен" << endl;
}

void PointStack::print() const {
    cout << "Содержимое стека (сверху вниз): ";
    if (container.isEmpty()) {
        cout << "пуст" << endl;
        return;
    }
    
    for (int i = container.getSize() - 1; i >= 0; i--) {
        container.getPoint(i).print();
        if (i > 0) {
            cout << " <- ";
        }
    }
    cout << endl;
}