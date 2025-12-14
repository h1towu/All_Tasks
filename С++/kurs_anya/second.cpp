#include <iostream>
#include <string>
#include <fstream>
using namespace std;

// БАЗОВЫЙ АБСТРАКТНЫЙ КЛАСС (добавили виртуальный метод)
class WeatherData {
public:
    virtual void show() = 0; // Чисто виртуальный метод - теперь это абстрактный класс
    virtual string getType() = 0; // Еще один виртуальный метод
    virtual ~WeatherData() {} // Виртуальный деструктор
};

// НАСЛЕДНИК 1: Дневная запись (основная)
class DailyWeather : public WeatherData {
public:
    string date;
    float temperature;
    float humidity;
    string condition;

    DailyWeather(string d, float temp, float hum, string cond) {
        date = d;
        temperature = temp;
        humidity = hum;
        condition = cond;
    }

    // ПЕРЕОПРЕДЕЛЕНИЕ виртуального метода (полиморфизм)
    void show() override {
        cout << "Тип: Дневная запись" << endl;
        cout << "Дата: " << date << endl;
        cout << "Температура: " << temperature << "C" << endl;
        cout << "Влажность: " << humidity << "%" << endl;
        cout << "Состояние: " << condition << endl;
        cout << "---------------------" << endl;
    }

    string getType() override {
        return "Дневная запись";
    }
};

// НАСЛЕДНИК 2: Ночная запись (простой пример наследования)
class NightWeather : public WeatherData {
public:
    string date;
    float temperature;
    float humidity;
    string moonPhase; // Дополнительное поле

    NightWeather(string d, float temp, float hum, string moon) {
        date = d;
        temperature = temp;
        humidity = hum;
        moonPhase = moon;
    }

    // ПЕРЕОПРЕДЕЛЕНИЕ с другим поведением (полиморфизм)
    void show() override {
        cout << "Тип: Ночная запись" << endl;
        cout << "Дата: " << date << endl;
        cout << "Температура: " << temperature << "C" << endl;
        cout << "Влажность: " << humidity << "%" << endl;
        cout << "Фаза луны: " << moonPhase << endl;
        cout << "---------------------" << endl;
    }

    string getType() override {
        return "Ночная запись";
    }
};

// Класс для системы мониторинга
class WeatherSystem {
private:
    WeatherData* records[100]; // Теперь храним указатели на БАЗОВЫЙ класс
    int count;

public:
    WeatherSystem() {
        count = 0;
        for (int i = 0; i < 100; i++) {
            records[i] = nullptr;
        }
        loadFromFile();
    }

    // Добавить дневную запись
    void addDailyRecord() {
        if (count >= 100) {
            cout << "Достигнут лимит записей!" << endl;
            return;
        }

        string date, condition;
        float temp, hum;

        cout << "\n=== НОВАЯ ДНЕВНАЯ ЗАПИСЬ ===" << endl;
        cout << "Введите дату (дд.мм.гггг): ";
        cin >> date;
        cout << "Введите температуру: ";
        cin >> temp;
        cout << "Введите влажность (%): ";
        cin >> hum;
        cout << "Введите состояние (солнечно/облачно/дождь): ";
        cin >> condition;

        // ПОЛИМОРФИЗМ: создаем объект наследника, храним как базовый класс
        records[count] = new DailyWeather(date, temp, hum, condition);
        count++;
        
        saveToFile();
        cout << "Дневная запись добавлена!" << endl;
    }

    // Добавить ночную запись (новая функция для демонстрации наследования)
    void addNightRecord() {
        if (count >= 100) {
            cout << "Достигнут лимит записей!" << endl;
            return;
        }

        string date, moonPhase;
        float temp, hum;

        cout << "\n=== НОВАЯ НОЧНАЯ ЗАПИСЬ ===" << endl;
        cout << "Введите дату (дд.мм.гггг): ";
        cin >> date;
        cout << "Введите температуру: ";
        cin >> temp;
        cout << "Введите влажность (%): ";
        cin >> hum;
        cout << "Введите фазу луны (полная/полумесяц/новая): ";
        cin >> moonPhase;

        // ПОЛИМОРФИЗМ: другой наследник, но тот же базовый тип
        records[count] = new NightWeather(date, temp, hum, moonPhase);
        count++;
        
        saveToFile();
        cout << "Ночная запись добавлена!" << endl;
    }

    // Показать все записи
    void showAll() {
        if (count == 0) {
            cout << "Нет записей" << endl;
            return;
        }

        cout << "\n=== ВСЕ ЗАПИСИ (" << count << ") ===" << endl;
        for (int i = 0; i < count; i++) {
            cout << "Запись #" << i + 1 << ":" << endl;
            // ПОЛИМОРФИЗМ: вызовется правильная версия show() для каждого объекта
            records[i]->show();
        }
    }

    // Показать статистику
    void showStats() {
        if (count == 0) {
            cout << "Нет данных для статистики" << endl;
            return;
        }

        float minTemp = 1000;
        float maxTemp = -1000;
        float sumTemp = 0;
        int dailyCount = 0;
        int nightCount = 0;

        for (int i = 0; i < count; i++) {
            // Динамическое приведение типа для доступа к полям
            DailyWeather* daily = dynamic_cast<DailyWeather*>(records[i]);
            NightWeather* night = dynamic_cast<NightWeather*>(records[i]);
            
            float temp = 0;
            if (daily) {
                temp = daily->temperature;
                dailyCount++;
            } else if (night) {
                temp = night->temperature;
                nightCount++;
            }

            sumTemp += temp;
            if (temp < minTemp) minTemp = temp;
            if (temp > maxTemp) maxTemp = temp;
        }

        cout << "\n=== СТАТИСТИКА ===" << endl;
        cout << "Всего записей: " << count << endl;
        cout << "Дневных записей: " << dailyCount << endl;
        cout << "Ночных записей: " << nightCount << endl;
        cout << "Самая низкая температура: " << minTemp << "C" << endl;
        cout << "Самая высокая температура: " << maxTemp << "C" << endl;
        if (count > 0) {
            cout << "Средняя температура: " << sumTemp / count << "C" << endl;
        }
    }

    // Показ записей по типу (демонстрация полиморфизма)
    void showByType() {
        if (count == 0) {
            cout << "Нет записей" << endl;
            return;
        }

        string type;
        cout << "Введите тип записи (дневная/ночная): ";
        cin >> type;

        cout << "\n=== ЗАПИСИ ТИПА: " << type << " ===" << endl;
        bool found = false;
        
        for (int i = 0; i < count; i++) {
            // ПОЛИМОРФИЗМ: вызываем виртуальный метод
            if (records[i]->getType() == type) {
                records[i]->show();
                found = true;
            }
        }

        if (!found) {
            cout << "Записей такого типа нет" << endl;
        }
    }

    // Сохранить данные в файл (упрощенная версия)
    void saveToFile() {
        ofstream file("weather_data.txt");
        if (!file.is_open()) return;

        for (int i = 0; i < count; i++) {
            // Просто сохраняем как дневные записи для простоты
            DailyWeather* daily = dynamic_cast<DailyWeather*>(records[i]);
            if (daily) {
                file << "DAY " << daily->date << " " 
                     << daily->temperature << " " 
                     << daily->humidity << " " 
                     << daily->condition << endl;
            }
        }
        file.close();
    }

    // Загрузить данные из файла
    void loadFromFile() {
        ifstream file("weather_data.txt");
        if (!file.is_open()) return;

        string type, date, condition;
        float temp, hum;
        
        while (file >> type >> date >> temp >> hum >> condition) {
            if (count < 100) {
                if (type == "DAY") {
                    records[count] = new DailyWeather(date, temp, hum, condition);
                    count++;
                }
            }
        }
        file.close();
    }

    // Деструктор
    ~WeatherSystem() {
        saveToFile();
        for (int i = 0; i < count; i++) {
            delete records[i]; // Корректно удаляем через виртуальный деструктор
        }
    }
};

// Главная функция
int main() {
    WeatherSystem system;
    int choice;

    do {
        cout << "\n=== СИСТЕМА МОНИТОРИНГА ПОГОДЫ (ООП) ===" << endl;
        cout << "1. Добавить дневную запись" << endl;
        cout << "2. Добавить ночную запись" << endl;
        cout << "3. Показать все записи" << endl;
        cout << "4. Статистика" << endl;
        cout << "5. Показать записи по типу" << endl;
        cout << "6. Выход" << endl;
        cout << "Выберите: ";
        cin >> choice;

        switch (choice) {
            case 1:
                system.addDailyRecord();
                break;
            case 2:
                system.addNightRecord();
                break;
            case 3:
                system.showAll();
                break;
            case 4:
                system.showStats();
                break;
            case 5:
                system.showByType();
                break;
            case 6:
                cout << "Выход из программы..." << endl;
                break;
            default:
                cout << "Неверный выбор!" << endl;
        }
    } while (choice != 6);

    return 0;
}