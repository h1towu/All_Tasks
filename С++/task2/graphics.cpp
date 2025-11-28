// graphics.cpp - реализации всех методов и функций
#include "graphics.h"
#include <iostream>
#include <cmath>

using namespace std;

// Реализация базового класса GraphicObject
GraphicObject::GraphicObject(const string& objName, int posX, int posY) 
    : name(objName), x(posX), y(posY) {
    cout << "Создан объект: " << name << endl;
}

GraphicObject::~GraphicObject() {
    cout << "Удален объект: " << name << endl;
}

void GraphicObject::draw() const {
    cout << "Рисую объект '" << name << "' в точке (" << x << ", " << y << ")" << endl;
}

void GraphicObject::move(int newX, int newY) {
    x = newX;
    y = newY;
    cout << "Объект '" << name << "' перемещен в (" << x << ", " << y << ")" << endl;
}

string GraphicObject::getName() const {
    return name;
}

// Реализация класса Circle
Circle::Circle(const string& name, int x, int y, double r) 
    : GraphicObject(name, x, y), radius(r) {
    cout << "Создан круг '" << name << "' радиусом " << radius << endl;
}

Circle::~Circle() {
    cout << "Удален круг '" << name << "'" << endl;
}

void Circle::draw() const {
    cout << "Рисую круг '" << name << "' в точке (" << x << ", " << y 
         << ") радиусом " << radius << endl;
}

double Circle::area() const {
    return 3.14159 * radius * radius;
}

double Circle::getRadius() const {
    return radius;
}

// Реализация класса Rectangle
Rectangle::Rectangle(const string& name, int x, int y, double w, double h) 
    : GraphicObject(name, x, y), width(w), height(h) {
    cout << "Создан прямоугольник '" << name << "' размером " << width << "x" << height << endl;
}

Rectangle::~Rectangle() {
    cout << "Удален прямоугольник '" << name << "'" << endl;
}

void Rectangle::draw() const {
    cout << "Рисую прямоугольник '" << name << "' в точке (" << x << ", " << y 
         << ") размером " << width << "x" << height << endl;
}

double Rectangle::area() const {
    return width * height;
}

double Rectangle::getWidth() const {
    return width;
}

double Rectangle::getHeight() const {
    return height;
}

// Реализация функций для работы с массивом объектов
void printAllObjects(const GraphicObject* objects[], int count) {
    cout << "=== Все объекты ===" << endl;
    for (int i = 0; i < count; i++) {
        if (objects[i] != nullptr) {
            objects[i]->draw();
            cout << "Площадь: " << objects[i]->area() << endl;
            cout << "---" << endl;
        }
    }
}

double totalArea(const GraphicObject* objects[], int count) {
    double total = 0.0;
    for (int i = 0; i < count; i++) {
        if (objects[i] != nullptr) {
            total += objects[i]->area();
        }
    }
    return total;
}