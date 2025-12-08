class Warehouse:
    def __init__(self, filename="warehouse.txt"):
        self.filename = filename
        self.items = self.load_items()

    def load_items(self):
        try:
            with open(self.filename, "r") as f:
                data = f.read().splitlines()
                items = {}
                for line in data:
                    # формат: название:количество:цена
                    name, qty, price = line.split(":")
                    items[name] = {"qty": int(qty), "price": float(price)}
                return items
        except:
            return {}

    def save_items(self):
        try:
            with open(self.filename, "w") as f:
                for name, data in self.items.items():
                    f.write(f"{name}:{data['qty']}:{data['price']}\n")
        except:
            print("Ошибка сохранения в файл")

    def add_item(self, name, qty, price):
        if qty <= 0 or price <= 0:
            print("Введите положительное число")
            return
        if name in self.items:
            self.items[name]["qty"] += qty
        else:
            self.items[name] = {"qty": qty, "price": price}
        self.save_items()

    def increase_item(self, name, qty=1):
        if name in self.items and qty > 0:
            self.items[name]["qty"] += qty
            self.save_items()

    def decrease_item(self, name, qty=1):
        if name not in self.items:
            print("Такого товара нет")
            return
        if qty <= 0:
            print("Введите положительное число")
            return
        if self.items[name]["qty"] < qty:
            print("Недостаточно на складе")
            return
        self.items[name]["qty"] -= qty
        if self.items[name]["qty"] == 0:
            del self.items[name]
        self.save_items()

    def show_items(self):
        return self.items

    def total_value(self):
        total = 0
        for data in self.items.values():
            total += data["qty"] * data["price"]
        return total
