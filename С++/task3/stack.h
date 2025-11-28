// stack.h - стек для точек на основе нашего контейнера
#ifndef STACK_H
#define STACK_H

#include "point_container.h"

class PointStack {
private:
    PointContainer container; // используем наш существующий контейнер

public:
    PointStack();
    
    // Добавление точки в стек
    void push(const Point& point);
    void push(double x, double y);
    
    // Удаление и возврат верхней точки
    Point pop();
    
    // Просмотр верхней точки без удаления
    Point peek() const;
    
    // Проверка на пустоту
    bool isEmpty() const;
    
    // Получение размера стека
    int getSize() const;
    
    // Очистка стека
    void clear();
    
    // Вывод содержимого стека
    void print() const;
};

#endif