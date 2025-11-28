import json

class Product:
    """Класс товара"""
    
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def show_info(self):
        """Показать информацию о товаре"""
        return f"ID: {self.product_id} | {self.name} | Цена: {self.price} руб. | Количество: {self.quantity} шт."

class Warehouse:
    """Класс склада"""
    
    def __init__(self):
        self.products = []
        self.next_id = 1
    
    def add_product(self, name, price, quantity):
        """Добавить товар на склад"""
        product = Product(self.next_id, name, price, quantity)
        self.products.append(product)
        self.next_id += 1
        print(f"✅ Товар '{name}' добавлен!")
    
    def show_all_products(self):
        """Показать все товары"""
        if not self.products:
            print("📭 Склад пуст!")
            return
        
        print("\n📦 ВСЕ ТОВАРЫ НА СКЛАДЕ:")
        for product in self.products:
            print(f"   {product.show_info()}")
    
    def find_product(self, product_id):
        """Найти товар по ID"""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def update_quantity(self, product_id, new_quantity):
        """Изменить количество товара"""
        product = self.find_product(product_id)
        if product:
            old_quantity = product.quantity
            product.quantity = new_quantity
            print(f"✅ Количество '{product.name}' изменено: {old_quantity} → {new_quantity}")
        else:
            print("❌ Товар не найден!")
    
    def remove_product(self, product_id):
        """Удалить товар"""
        product = self.find_product(product_id)
        if product:
            self.products.remove(product)
            print(f"✅ Товар '{product.name}' удален!")
        else:
            print("❌ Товар не найден!")
    
    def save_to_file(self):
        """Сохранить данные в файл"""
        data = {
            'next_id': self.next_id,
            'products': []
        }
        
        for product in self.products:
            data['products'].append({
                'id': product.product_id,
                'name': product.name,
                'price': product.price,
                'quantity': product.quantity
            })
        
        with open('warehouse.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("💾 Данные сохранены!")
    
    def load_from_file(self):
        """Загрузить данные из файла"""
        try:
            with open('warehouse.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.products = []
            for product_data in data['products']:
                product = Product(
                    product_data['id'],
                    product_data['name'],
                    product_data['price'],
                    product_data['quantity']
                )
                self.products.append(product)
            
            self.next_id = data['next_id']
            print("📂 Данные загружены!")
            return True
        except FileNotFoundError:
            print("📂 Файл не найден. Создан новый склад.")
            return False

def main():
    """Главная функция программы"""
    warehouse = Warehouse()
    warehouse.load_from_file()
    
    while True:
        print("\n" + "="*50)
        print("🏭 СИСТЕМА СКЛАДСКОГО УЧЕТА")
        print("="*50)
        print("1. 📥 Добавить товар")
        print("2. 📦 Показать все товары")
        print("3. ✏️  Изменить количество")
        print("4. 🗑️  Удалить товар")
        print("5. 💾 Сохранить данные")
        print("0. ❌ Выйти")
        print("-"*50)
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            print("\n📥 ДОБАВЛЕНИЕ ТОВАРА")
            name = input("Название товара: ")
            price = float(input("Цена: "))
            quantity = int(input("Количество: "))
            warehouse.add_product(name, price, quantity)
        
        elif choice == "2":
            warehouse.show_all_products()
        
        elif choice == "3":
            print("\n✏️ ИЗМЕНЕНИЕ КОЛИЧЕСТВА")
            warehouse.show_all_products()
            product_id = int(input("Введите ID товара: "))
            new_quantity = int(input("Новое количество: "))
            warehouse.update_quantity(product_id, new_quantity)
        
        elif choice == "4":
            print("\n🗑️ УДАЛЕНИЕ ТОВАРА")
            warehouse.show_all_products()
            product_id = int(input("Введите ID товара для удаления: "))
            warehouse.remove_product(product_id)
        
        elif choice == "5":
            warehouse.save_to_file()
        
        elif choice == "0":
            warehouse.save_to_file()
            print("👋 До свидания!")
            break
        
        else:
            print("❌ Неверный выбор!")

# Запуск программы
if __name__ == "__main__":
    main()