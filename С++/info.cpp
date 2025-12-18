#include <iostream>
#include <string>
#include <vector>
#include <fstream>

using namespace std;

// АБСТРАКЦИЯ: базовый класс для наблюдения за погодой
class WeatherObservation {
private:
    // ИНКАПСУЛЯЦИЯ: поля скрыты
    string location;
    string date;
    double temperature;
    int humidity;
    
public:
    // Конструктор
    WeatherObservation(string loc, double temp, int hum, string dt) 
        : location(loc), temperature(temp), humidity(hum), date(dt) {}
    
    // Виртуальный метод для отображения информации
    virtual void display() const {
        cout << "Место: " << location << ", Дата: " << date;
        cout << ", Температура: " << temperature << "°C, Влажность: " << humidity << "%" << endl;
    }
    
    // Геттеры
    string getLocation() const { return location; }
    string getDate() const { return date; }
    double getTemperature() const { return temperature; }
    int getHumidity() const { return humidity; }
    
    // Виртуальный деструктор
    virtual ~WeatherObservation() {}
};

// НАСЛЕДОВАНИЕ: класс для расширенного наблюдения с ветром
class ExtendedWeatherObservation : public WeatherObservation {
private:
    double windSpeed; // скорость ветра в м/с
    string windDirection;
    
public:
    ExtendedWeatherObservation(string loc, double temp, int hum, double ws, string wd, string dt) 
        : WeatherObservation(loc, temp, hum, dt), windSpeed(ws), windDirection(wd) {}
    
    // ПОЛИМОРФИЗМ: переопределение метода display
    void display() const override {
        cout << "МЕСТО: " << getLocation() << ", ДАТА: " << getDate();
        cout << ", ТЕМПЕРАТУРА: " << getTemperature() << "°C, ";
        cout << "ВЛАЖНОСТЬ: " << getHumidity() << "%, ";
        cout << "ВЕТЕР: " << windSpeed << " м/с, ";
        cout << "НАПРАВЛЕНИЕ ВЕТРА: " << windDirection << endl;
    }
    
    double getWindSpeed() const { return windSpeed; }
    string getWindDirection() const { return windDirection; }
};

// Класс для управления системой мониторинга
class WeatherMonitoringSystem {
private:
    vector<WeatherObservation*> observations;
    string filename = "weather_data.txt";
    
    // Простая функция для ввода даты
    string askForDate() {
        string date_input;
        cout << "Введите дату в формате Д.М.ГГГГ (например, 1.1.2025): ";
        cin >> date_input;
        return date_input;
    }
    
public:
    // Деструктор для очистки памяти
    ~WeatherMonitoringSystem() {
        for (auto observation : observations) {
            delete observation;
        }
    }
    
    // Добавление наблюдения
    void addObservation() {
        string location;
        double temperature;
        int humidity;
        
        cout << "Введите место наблюдения: ";
        cin.ignore();
        getline(cin, location);
        
        cout << "Введите температуру (°C): ";
        cin >> temperature;
        
        cout << "Введите влажность (%): ";
        cin >> humidity;
        
        // Запрашиваем дату
        string observation_date = askForDate();
        
        char choice;
        cout << "Добавить данные о ветре? (y/n): ";
        cin >> choice;
        
        if (choice == 'y' || choice == 'Y') {
            double windSpeed;
            string windDirection;
            
            cout << "Введите скорость ветра (м/с): ";
            cin >> windSpeed;
            
            cout << "Введите направление ветра: ";
            cin >> windDirection;
            
            observations.push_back(new ExtendedWeatherObservation(location, temperature, humidity, windSpeed, windDirection, observation_date));
        } else {
            observations.push_back(new WeatherObservation(location, temperature, humidity, observation_date));
        }
        
        cout << "Наблюдение добавлено!" << endl;
    }
    
    // Удаление наблюдения
    void removeObservation() {
        if (observations.empty()) {
            cout << "Нет наблюдений!" << endl;
            return;
        }
        
        showObservations();
        
        int index;
        cout << "Введите номер наблюдения для удаления: ";
        cin >> index;
        
        if (index >= 1 && index <= observations.size()) {
            delete observations[index - 1];
            observations.erase(observations.begin() + (index - 1));
            cout << "Наблюдение удалено!" << endl;
        } else {
            cout << "Неверный номер!" << endl;
        }
    }
    
    // Показать все наблюдения
    void showObservations() const {
        if (observations.empty()) {
            cout << "Нет наблюдений!" << endl;
            return;
        }
        
        cout << "\n=== ИСТОРИЯ НАБЛЮДЕНИЙ ЗА ПОГОДОЙ ===" << endl;
        for (size_t i = 0; i < observations.size(); i++) {
            cout << i + 1 << ". ";
            observations[i]->display();
        }
        cout << "====================================\n" << endl;
    }
    
    // Показать средние показатели
    void showAverage() const {
        if (observations.empty()) {
            cout << "Нет данных для расчета!" << endl;
            return;
        }
        
        double totalTemp = 0;
        int totalHumidity = 0;
        int count = 0;
        
        for (const auto& obs : observations) {
            totalTemp += obs->getTemperature();
            totalHumidity += obs->getHumidity();
            count++;
        }
        
        cout << "\n=== СРЕДНИЕ ПОКАЗАТЕЛИ ===" << endl;
        cout << "Средняя температура: " << totalTemp / count << "°C" << endl;
        cout << "Средняя влажность: " << totalHumidity / count << "%" << endl;
        cout << "Всего наблюдений: " << count << endl;
        cout << "=========================\n" << endl;
    }
    
    // Автоматическое сохранение в файл
    void saveToFile() {
        ofstream file(filename);
        
        if (!file.is_open()) {
            cout << "Ошибка при сохранении данных!" << endl;
            return;
        }
        
        file << observations.size() << endl;
        
        for (const auto& obs : observations) {
            ExtendedWeatherObservation* extended = dynamic_cast<ExtendedWeatherObservation*>(obs);
            
            if (extended) {
                file << "1 " << obs->getLocation() << " " 
                     << obs->getTemperature() << " " 
                     << obs->getHumidity() << " "
                     << extended->getWindSpeed() << " "
                     << extended->getWindDirection() << " "
                     << obs->getDate() << endl;
            } else {
                file << "0 " << obs->getLocation() << " " 
                     << obs->getTemperature() << " " 
                     << obs->getHumidity() << " "
                     << obs->getDate() << endl;
            }
        }
        
        file.close();
    }
    
    // Автоматическое чтение из файла
    void loadFromFile() {
        ifstream file(filename);
        
        if (!file.is_open()) {
            cout << "Файл данных не найден. Будет создан новый." << endl;
            return;
        }
        
        for (auto obs : observations) {
            delete obs;
        }
        observations.clear();
        
        int count;
        file >> count;
        
        for (int i = 0; i < count; i++) {
            int type;
            file >> type;
            
            string location;
            double temperature;
            int humidity;
            string date;
            
            file >> location >> temperature >> humidity >> date;
            
            if (type == 1) {
                double windSpeed;
                string windDirection;
                file >> windSpeed >> windDirection;
                observations.push_back(new ExtendedWeatherObservation(location, temperature, humidity, windSpeed, windDirection, date));
            } else {
                observations.push_back(new WeatherObservation(location, temperature, humidity, date));
            }
        }
        
        file.close();
        cout << "Данные о погоде загружены!" << endl;
    }
};

// Главная функция
int main() {
    WeatherMonitoringSystem weatherSystem;
    
    weatherSystem.loadFromFile();
    
    int choice = 0;
    
    do {
        cout << "\n=== СИСТЕМА МОНИТОРИНГА ПОГОДЫ ===" << endl;
        cout << "1. Добавить наблюдение" << endl;
        cout << "2. Удалить наблюдение" << endl;
        cout << "3. Показать все наблюдения" << endl;
        cout << "4. Показать средние показатели" << endl;
        cout << "5. Выход" << endl;
        cout << "Выберите действие: ";
        cin >> choice;
        
        switch (choice) {
            case 1:
                weatherSystem.addObservation();
                weatherSystem.saveToFile();
                break;
                
            case 2:
                weatherSystem.removeObservation();
                weatherSystem.saveToFile();
                break;
                
            case 3:
                weatherSystem.showObservations();
                break;
                
            case 4:
                weatherSystem.showAverage();
                break;
                
            case 5:
                cout << "Выход из программы..." << endl;
                break;
                
            default:
                cout << "Неверный выбор!" << endl;
        }
        
    } while (choice != 5);
    
    return 0;
}