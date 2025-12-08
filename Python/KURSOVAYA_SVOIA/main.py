class WarehouseItem:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

class WarehouseSystem:
    def __init__(self):
        self.items = []

    def add_item(self):

        name = input("Введите название товара: ")
        quantity = int(input("Введите количество товара: "))
        price = int(input("Введите цену товара: "))
        item = WarehouseItem(name, quantity, price)
        self.items.append(item)
        print("\nТовар успешно добавлен!")
    def remove_item(self):
        name = input("\nВведите название товара, который вы хотите удалить: ")
        for item in self.items:
            if item.name == name:
                self.items.remove(item)
                print("\nТовар успешно удален!")
                break
        else:
            print("\nТовар не найден!")

    def show_item(self):
        if self.items is None: print('\nТоваров нет')

        else:
            for item in self.items:
                        print(f"\nНазвание: {item.name} Количество: {item.quantity} Цена: {item.price}")

            
class WarehouseApp:
    def __init__(self):
         self.system = WarehouseSystem()
    def run(self):
         while True:
            print("\n1. Добавить товар")
            print("2. Удалить товар")
            print("3. Показать товары")
            print("4. Выход")
            choice = input("\nВыберите действие: ")
            if choice == "1":
                self.system.add_item()
            elif choice == "2":
                self.system.remove_item()
            elif choice == "3":
                self.system.show_item()
            elif choice == "4":
                break

app = WarehouseApp()
app.run()