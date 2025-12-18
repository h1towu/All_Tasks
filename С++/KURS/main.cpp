#include <iostream>
#include <string>
#include <vector>
#include <fstream>

using namespace std;

// АБСТРАКЦИЯ: базовый класс для товара
class Product {
private:
    // ИНКАПСУЛЯЦИЯ: поля скрыты
    string name;
    int quantity;
    double price;

public:
    // Конструктор
    Product(string n, int q, double p) : name(n), quantity(q), price(p) {}

    // Виртуальный метод для отображения информации
    virtual void display() const {
        cout << "Товар: " << name << ", Количество: " << quantity << ", Цена: " << price << " руб." << endl;
    }

    // геттеры
    string getName() const { return name; }
    int getQuantity() const { return quantity; }
    double getPrice() const { return price; }

    // сеттеры
    void setQuantity(int q) { quantity = q; }
    void setPrice(double p) { price = p; }

    // Виртуальный деструктор
    virtual ~Product() {}
};

// НАСЛЕДОВАНИЕ: создаем производный класс
class WeightProduct : public Product {
private:
    double weight;
    string unit;

public:
    WeightProduct(string n, int q, double p, double w, string u)
        : Product(n, q, p), weight(w), unit(u) {
    }

    // ПОЛИМОРФИЗМ: переопределение метода display
    void display() const override {
        cout << "Весовой товар: " << getName() << ", Количество: " << getQuantity()
            << ", Цена: " << getPrice() << " руб., Вес: " << weight << " " << unit << endl;
    }

    double getWeight() const { return weight; }
    string getUnit() const { return unit; }
};

// НАСЛЕДОВАНИЕ: еще один производный класс
class FragileProduct : public Product {
private:
    string packagingType;

public:
    FragileProduct(string n, int q, double p, string pt)
        : Product(n, q, p), packagingType(pt) {
    }

    // ПОЛИМОРФИЗМ: переопределение метода display
    void display() const override {
        cout << "Хрупкий товар: " << getName() << ", Количество: " << getQuantity()
            << ", Цена: " << getPrice() << " руб., Упаковка: " << packagingType << endl;
    }

    string getPackagingType() const { return packagingType; }
};


class Warehouse {
private:
    // ИНКАПСУЛЯЦИЯ: вектор товаров скрыт внутри класса
    vector<Product*> products;
    string filename = "warehouse_data.txt";

public:
    // Деструктор для очистки памяти
    ~Warehouse() {
        for (auto product : products) {
            delete product;
        }
    }

    // Добавление товара с выбором типа
    void addProduct() {
        int productType;
        string name;
        int quantity;
        double price;

        cout << "\nВЫБОР ТИПА ТОВАРА" << endl;
        cout << "1. Обычный товар" << endl;
        cout << "2. Весовой товар" << endl;
        cout << "3. Хрупкий товар" << endl;
        cout << "Выберите тип товара: ";
        cin >> productType;

        cout << "Введите название товара: ";
        cin.ignore();
        getline(cin, name);

        cout << "Введите количество: ";
        cin >> quantity;

        cout << "Введите цену: ";
        cin >> price;

        // ПОЛИМОРФИЗМ: создаем объекты разных типов через указатель на базовый класс
        switch (productType) {
        case 1: // Обычный товар
            products.push_back(new Product(name, quantity, price));
            break;

        case 2: // Весовой товар
        {
            double weight;
            string unit;
            cout << "Введите вес: ";
            cin >> weight;
            cout << "Введите единицу измерения (кг/г/т): ";
            cin >> unit;
            products.push_back(new WeightProduct(name, quantity, price, weight, unit));
            break;
        }

        case 3: // Хрупкий товар
        {
            string packaging;
            cout << "Введите тип упаковки: ";
            cin.ignore();
            getline(cin, packaging);
            products.push_back(new FragileProduct(name, quantity, price, packaging));
            break;
        }

        default:
            cout << "Неверный тип товара. Добавлен обычный товар." << endl;
            products.push_back(new Product(name, quantity, price));
            break;
        }

        cout << "Товар добавлен" << endl;
    }

    void removeProduct() {
        if (products.empty()) {
            cout << "Склад пуст" << endl;
            return;
        }

        showProducts();

        int index;
        cout << "Введите номер товара для удаления: ";
        cin >> index;

        if (index >= 1 && index <= products.size()) {
            delete products[index - 1];
            products.erase(products.begin() + (index - 1));
            cout << "Товар удален" << endl;
        }
        else {
            cout << "Неверный номер" << endl;
        }
    }

    void showProducts() const {
        if (products.empty()) {
            cout << "Склад пуст!" << endl;
            return;
        }

        cout << "\nСПИСОК ТОВАРОВ" << endl;
        // ПОЛИМОРФИЗМ: вызов метода display для объектов разных типов
        for (size_t i = 0; i < products.size(); i++) {
            cout << i + 1 << ". ";
            products[i]->display();
        }
        cout << "====================\n" << endl;
    }

    void saveToFile() {
        ofstream file(filename);

        if (!file.is_open()) {
            cout << "Ошибка при сохранении данных" << endl;
            return;
        }

        file << products.size() << endl;

        for (const auto& product : products) {
            file << product->getName() << " "
                << product->getQuantity() << " "
                << product->getPrice() << endl;
        }

        file.close();
    }

    void loadFromFile() {
        ifstream file(filename);

        if (!file.is_open()) {
            cout << "Файл данных не найден. Будет создан новый." << endl;
            return;
        }

        for (auto product : products) {
            delete product;
        }
        products.clear();

        int count;
        file >> count;

        for (int i = 0; i < count; i++) {
            string name;
            int quantity;
            double price;

            file >> name >> quantity >> price;
            products.push_back(new Product(name, quantity, price));
        }

        file.close();
        cout << "Данные загружены" << endl;
    }
};

int main() {

    Warehouse warehouse;

    warehouse.loadFromFile();

    int choice = 0;

    do {
        cout << "\nСИСТЕМА СКЛАДСКОГО УЧЕТА" << endl;
        cout << "1. Добавить товар" << endl;
        cout << "2. Удалить товар" << endl;
        cout << "3. Показать товары" << endl;
        cout << "4. Выход" << endl;
        cout << "Выберите действие: ";
        cin >> choice;

        switch (choice) {
        case 1:
            warehouse.addProduct();
            warehouse.saveToFile(); 
            break;

        case 2:
            warehouse.removeProduct();
            warehouse.saveToFile(); 
            break;

        case 3:
            warehouse.showProducts();
            break;

        case 4:
            cout << "Выход из программы..." << endl;
            break;

        default:
            cout << "Неверный выбор" << endl;
        }

    } while (choice != 4);

    return 0;
}