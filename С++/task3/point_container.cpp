// point_container.cpp - реализация контейнера точек
#include "point_container.h"
#include <iostream>
#include <algorithm> // для std::copy

using namespace std;

PointContainer::PointContainer() : capacity(10), size(0) {
    points = new Point[capacity];
}

PointContainer::~PointContainer() {
    delete[] points;
}

PointContainer::PointContainer(const PointContainer& other) 
    : capacity(other.capacity), size(other.size) {
    points = new Point[capacity];
    for (int i = 0; i < size; i++) {
        points[i] = other.points[i];
    }
}

PointContainer& PointContainer::operator=(const PointContainer& other) {
    if (this != &other) {
        delete[] points;
        
        capacity = other.capacity;
        size = other.size;
        points = new Point[capacity];
        
        for (int i = 0; i < size; i++) {
            points[i] = other.points[i];
        }
    }
    return *this;
}

void PointContainer::resize() {
    capacity *= 2;
    Point* newPoints = new Point[capacity];
    
    for (int i = 0; i < size; i++) {
        newPoints[i] = points[i];
    }
    
    delete[] points;
    points = newPoints;
    
    cout << "Контейнер увеличен до " << capacity << " элементов" << endl;
}

void PointContainer::addPoint(const Point& point) {
    if (size >= capacity) {
        resize();
    }
    
    points[size] = point;
    size++;
    cout << "Точка добавлена в контейнер. Всего точек: " << size << endl;
}

void PointContainer::removePoint(int index) {
    if (index < 0 || index >= size) {
        cout << "Ошибка: неверный индекс!" << endl;
        return;
    }
    
    for (int i = index; i < size - 1; i++) {
        points[i] = points[i + 1];
    }
    size--;
    
    cout << "Точка удалена из контейнера. Осталось точек: " << size << endl;
}

Point PointContainer::getPoint(int index) const {
    if (index < 0 || index >= size) {
        cout << "Ошибка: неверный индекс! Возвращена точка (0,0)" << endl;
        return Point(0, 0);
    }
    return points[index];
}

void PointContainer::setPoint(int index, const Point& point) {
    if (index < 0 || index >= size) {
        cout << "Ошибка: неверный индекс!" << endl;
        return;
    }
    points[index] = point;
}

int PointContainer::getSize() const {
    return size;
}

bool PointContainer::isEmpty() const {
    return size == 0;
}

void PointContainer::clear() {
    size = 0;
    cout << "Контейнер очищен" << endl;
}

int PointContainer::findPoint(const Point& point) const {
    for (int i = 0; i < size; i++) {
        if (points[i].getX() == point.getX() && points[i].getY() == point.getY()) {
            return i;
        }
    }
    return -1;
}