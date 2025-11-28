// polyline.h - класс ломаной линии с использованием контейнера
#ifndef POLYLINE_H
#define POLYLINE_H

#include "point_container.h"
#include <string>

class Polyline {
private:
    std::string name;
    PointContainer points; // используем наш контейнер

public:
    Polyline(const std::string& name = "Unnamed Polyline");
    
    // Добавление точки в ломаную
    void addPoint(const Point& point);
    void addPoint(double x, double y);
    
    // Удаление точки
    void removePoint(int index);
    
    // Получение точки
    Point getPoint(int index) const;
    
    // Получение количества точек
    int getPointCount() const;
    
    // Расчет длины ломаной
    double calculateLength() const;
    
    // Вывод информации
    void print() const;
    
    // Очистка ломаной
    void clear();
    
    // Проверка на пустоту
    bool isEmpty() const;
    
    std::string getName() const;
    void setName(const std::string& name);
};

#endif