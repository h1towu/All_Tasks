// main.cpp - использование графических объектов
#include "graphics.h"
#include <iostream>

using namespace std;

int main() {
    cout << "=== Программа для работы с графическими объектами ===" << endl;
    
    // Создаем несколько графических объектов
    Circle circle1("Красный круг", 10, 20, 5.0);
    Circle circle2("Синий круг", 30, 40, 7.5);
    Rectangle rect1("Зеленый прямоугольник", 50, 60, 8.0, 6.0);
    Rectangle rect2("Желтый прямоугольник", 70, 80, 12.0, 4.0);
    
    cout << endl << "=== Информация об объектах ===" << endl;
    
    // Используем полиморфизм через массив указателей
    const GraphicObject* objects[] = {&circle1, &circle2, &rect1, &rect2};
    const int objectCount = 4;
    
    // Выводим информацию обо всех объектах
    printAllObjects(objects, objectCount);
    
    // Вычисляем общую площадь
    double total = totalArea(objects, objectCount);
    cout << "Общая площадь всех объектов: " << total << endl;
    
    cout << endl << "=== Тестирование отдельных методов ===" << endl;
    
    // Тестируем методы отдельных объектов
    cout << "Площадь '" << circle1.getName() << "': " << circle1.area() << endl;
    cout << "Площадь '" << rect1.getName() << "': " << rect1.area() << endl;
    
    // Перемещаем объекты
    circle1.move(100, 200);
    rect1.move(150, 250);
    
    cout << endl << "=== Финальная информация ===" << endl;
    printAllObjects(objects, objectCount);
    
    cout << "Программа завершена!" << endl;
    return 0;
}
/*
g++ -c graphics.cpp -o graphics.o
g++ -c main.cpp -o main.o

g++ graphics.o main.o -o graphics_program

./graphics_program
*/