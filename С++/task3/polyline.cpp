// polyline.cpp - реализация ломаной линии
#include "polyline.h"
#include <iostream>

using namespace std;

Polyline::Polyline(const std::string& name) : name(name) {
    cout << "Создана ломаная: " << name << endl;
}

void Polyline::addPoint(const Point& point) {
    points.addPoint(point);
    cout << "Точка добавлена в ломаную '" << name << "'" << endl;
}

void Polyline::addPoint(double x, double y) {
    Point point(x, y);
    points.addPoint(point);
}

void Polyline::removePoint(int index) {
    if (index < 0 || index >= points.getSize()) {
        cout << "Ошибка: неверный индекс точки!" << endl;
        return;
    }
    points.removePoint(index);
    cout << "Точка удалена из ломаной '" << name << "'" << endl;
}

Point Polyline::getPoint(int index) const {
    return points.getPoint(index);
}

int Polyline::getPointCount() const {
    return points.getSize();
}

double Polyline::calculateLength() const {
    if (points.getSize() < 2) {
        return 0.0;
    }
    
    double length = 0.0;
    for (int i = 0; i < points.getSize() - 1; i++) {
        Point current = points.getPoint(i);
        Point next = points.getPoint(i + 1);
        length += current.distanceTo(next);
    }
    
    return length;
}

void Polyline::print() const {
    cout << "Ломаная '" << name << "': ";
    cout << "точек = " << points.getSize() << ", ";
    cout << "длина = " << calculateLength() << endl;
    
    cout << "Точки: ";
    for (int i = 0; i < points.getSize(); i++) {
        points.getPoint(i).print();
        if (i < points.getSize() - 1) {
            cout << " -> ";
        }
    }
    cout << endl;
}

void Polyline::clear() {
    points.clear();
    cout << "Ломаная '" << name << "' очищена" << endl;
}

bool Polyline::isEmpty() const {
    return points.isEmpty();
}

std::string Polyline::getName() const {
    return name;
}

void Polyline::setName(const std::string& name) {
    this->name = name;
}