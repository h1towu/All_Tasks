// point.cpp - реализация класса точки
#include "point.h"
#include <cmath>
#include <iostream>

using namespace std;

Point::Point(double x, double y) : x(x), y(y) {
    cout << "Создана точка (" << x << ", " << y << ")" << endl;
}

double Point::getX() const {
    return x;
}

double Point::getY() const {
    return y;
}

void Point::setX(double x) {
    this->x = x;
}

void Point::setY(double y) {
    this->y = y;
}

void Point::print() const {
    cout << "(" << x << ", " << y << ")";
}

double Point::distanceTo(const Point& other) const {
    return sqrt(pow(x - other.x, 2) + pow(y - other.y, 2));
}