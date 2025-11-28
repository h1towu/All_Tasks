// point_container.h - контейнер для хранения точек
#ifndef POINT_CONTAINER_H
#define POINT_CONTAINER_H

#include "point.h" // Предполагаем, что у нас уже есть класс Point

class PointContainer {
private:
    Point* points;       // динамический массив точек
    int capacity;        // вместимость массива
    int size;           // текущее количество точек
    
    void resize();      // увеличение вместимости массива

public:
    PointContainer();
    ~PointContainer();
    
    // Конструктор копирования
    PointContainer(const PointContainer& other);
    
    // Оператор присваивания
    PointContainer& operator=(const PointContainer& other);
    
    // Добавление точки
    void addPoint(const Point& point);
    
    // Удаление точки по индексу
    void removePoint(int index);
    
    // Получение точки по индексу
    Point getPoint(int index) const;
    
    // Изменение точки по индексу
    void setPoint(int index, const Point& point);
    
    // Получение количества точек
    int getSize() const;
    
    // Проверка на пустоту
    bool isEmpty() const;
    
    // Очистка контейнера
    void clear();
    
    // Поиск точки (возвращает индекс или -1)
    int findPoint(const Point& point) const;
};

#endif