// point.h - класс точки
#ifndef POINT_H
#define POINT_H

#include <iostream>

class Point {
private:
    double x, y;

public:
    Point(double x = 0, double y = 0);
    
    // Геттеры
    double getX() const;
    double getY() const;
    
    // Сеттеры
    void setX(double x);
    void setY(double y);
    
    // Вывод информации
    void print() const;
    
    // Расчет расстояния до другой точки
    double distanceTo(const Point& other) const;
};

#endif