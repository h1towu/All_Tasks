#include <iostream>
#include <string>
#include <fstream>
using namespace std;

// Класс для одной записи о погоде
class WeatherRecord {
public:
    string date;        // Только дата
    float temperature;
    float humidity;
    string condition;   // Состояние: солнечно, облачно, дождь

    // Конструктор
    WeatherRecord(string d, float temp, float hum, string cond) {
        date = d;
        temperature = temp;
        humidity = hum;
        condition = cond;
    }

    // Метод для отображения записи
    void show() {
        cout << "Дата: " << date << endl;
        cout << "Температура: " << temperature << "C" << endl;
        cout << "Влажность: " << humidity << "%" << endl;
        cout << "Состояние: " << condition << endl;
        cout << "---------------------" << endl;
    }
};

// Класс для системы мониторинга
class WeatherSystem {
private:
    WeatherRecord* records[100]; // Массив указателей на записи
    int count; // Количество записей

public:
    WeatherSystem() {
        count = 0;
        for (int i = 0; i < 100; i++) {
            records[i] = nullptr;
        }
        loadFromFile(); // Автоматически загружаем данные при запуске
    }

    // Добавить новую запись
    void addRecord() {
        if (count >= 100) {
            cout << "Достигнут лимит записей!" << endl;
            return;
        }

        string date, condition;
        float temp, hum;

        cout << "\n=== НОВАЯ ЗАПИСЬ ===" << endl;
        cout << "Введите дату (дд.мм.гггг): ";
        cin >> date;
        cout << "Введите температуру: ";
        cin >> temp;
        cout << "Введите влажность (%): ";
        cin >> hum;
        cout << "Введите состояние (солнечно/облачно/дождь): ";
        cin >> condition;

        records[count] = new WeatherRecord(date, temp, hum, condition);
        count++;
        
        saveToFile(); // Автоматически сохраняем в файл
        cout << "Запись добавлена!" << endl;
    }

    // Показать все записи
    void showAll() {
        if (count == 0) {
            cout << "Нет записей" << endl;
            return;
        }

        cout << "\n=== ВСЕ ЗАПИСИ (" << count << ") ===" << endl;
        for (int i = 0; i < count; i++) {
            cout << "День #" << i + 1 << ":" << endl;
            records[i]->show();
        }
    }

    // Показать статистику
    void showStats() {
        if (count == 0) {
            cout << "Нет данных для статистики" << endl;
            return;
        }

        float minTemp = records[0]->temperature;
        float maxTemp = records[0]->temperature;
        float sumTemp = 0;
        float sumHum = 0;
        int sunnyDays = 0;
        int cloudyDays = 0;
        int rainyDays = 0;

        for (int i = 0; i < count; i++) {
            float temp = records[i]->temperature;
            sumTemp += temp;
            sumHum += records[i]->humidity;

            if (temp < minTemp) minTemp = temp;
            if (temp > maxTemp) maxTemp = temp;

            // Считаем дни по состояниям
            if (records[i]->condition == "солнечно") sunnyDays++;
            else if (records[i]->condition == "облачно") cloudyDays++;
            else if (records[i]->condition == "дождь") rainyDays++;
        }

        cout << "\n=== СТАТИСТИКА ===" << endl;
        cout << "Всего дней: " << count << endl;
        cout << "Самая низкая температура: " << minTemp << "C" << endl;
        cout << "Самая высокая температура: " << maxTemp << "C" << endl;
        cout << "Средняя температура: " << sumTemp / count << "C" << endl;
        cout << "Средняя влажность: " << sumHum / count << "%" << endl;
        cout << "Солнечных дней: " << sunnyDays << endl;
        cout << "Облачных дней: " << cloudyDays << endl;
        cout << "Дождливых дней: " << rainyDays << endl;
    }

    // Сохранить данные в файл
    void saveToFile() {
        ofstream file("weather_data.txt");
        
        if (!file.is_open()) {
            cout << "Ошибка сохранения файла!" << endl;
            return;
        }

        for (int i = 0; i < count; i++) {
            file << records[i]->date << " "
                 << records[i]->temperature << " "
                 << records[i]->humidity << " "
                 << records[i]->condition << endl;
        }

        file.close();
    }

    // Загрузить данные из файла
    void loadFromFile() {
        ifstream file("weather_data.txt");
        
        if (!file.is_open()) {
            return; // Файла нет - это нормально при первом запуске
        }

        string date, condition;
        float temp, hum;
        
        while (file >> date >> temp >> hum >> condition) {
            if (count < 100) {
                records[count] = new WeatherRecord(date, temp, hum, condition);
                count++;
            }
        }

        file.close();
    }

    // Деструктор для очистки памяти
    ~WeatherSystem() {
        saveToFile(); // Автоматически сохраняем при выходе
        for (int i = 0; i < count; i++) {
            delete records[i];
        }
    }
};

// Главная функция
int main() {
    WeatherSystem system;
    int choice;

    do {
        cout << "\n=== СИСТЕМА МОНИТОРИНГА ПОГОДЫ ===" << endl;
        cout << "1. Добавить запись за день" << endl;
        cout << "2. Показать все дни" << endl;
        cout << "3. Статистика" << endl;
        cout << "4. Выход" << endl;
        cout << "Выберите: ";
        cin >> choice;

        switch (choice) {
            case 1:
                system.addRecord();
                break;
            case 2:
                system.showAll();
                break;
            case 3:
                system.showStats();
                break;
            case 4:
                cout << "Выход из программы..." << endl;
                break;
            default:
                cout << "Неверный выбор!" << endl;
        }
    } while (choice != 4);

    return 0;
}