// graphics.h - только объявления классов и функций
#ifndef GRAPHICS_H
#define GRAPHICS_H

#include <string>

// Базовый класс для всех графических объектов
class GraphicObject {
protected:
    std::string name;
    int x, y; // координаты
    
public:
    GraphicObject(const std::string& objName, int posX, int posY);
    virtual ~GraphicObject();
    
    virtual void draw() const; // виртуальная функция рисования
    virtual double area() const = 0; // чисто виртуальная функция
    
    void move(int newX, int newY);
    std::string getName() const;
};

// Класс для круга
class Circle : public GraphicObject {
private:
    double radius;
    
public:
    Circle(const std::string& name, int x, int y, double r);
    ~Circle();
    
    void draw() const override;
    double area() const override;
    
    double getRadius() const;
};

// Класс для прямоугольника
class Rectangle : public GraphicObject {
private:
    double width, height;
    
public:
    Rectangle(const std::string& name, int x, int y, double w, double h);
    ~Rectangle();
    
    void draw() const override;
    double area() const override;
    
    double getWidth() const;
    double getHeight() const;
};

// Объявления функций для работы с массивом объектов
void printAllObjects(const GraphicObject* objects[], int count);
double totalArea(const GraphicObject* objects[], int count);

#endif