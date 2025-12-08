class WarehouseItem:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

class WarehouseSystem:
    def __init__(self, filename='warehouse.txt'):
        self.items = []
        self.filename = filename
        self.load_from_file()
    
    def add_item(self, name, quantity, price):

        item = WarehouseItem(name, quantity, price)
        self.items.append(item)
        self.save_to_file()
        return f"Товар '{name}' успешно добавлен!"
    
    def remove_item(self, name):

        for item in self.items:
            if item.name == name:
                self.items.remove(item)
                self.save_to_file()
                return f"Товар '{name}' успешно удален!"
        return f"Товар '{name}' не найден!"
    
    def get_all_items(self):

        return self.items
    
    def get_items_count(self):

        return len(self.items)
    
    def get_total_value(self):

        return sum(item.price * item.quantity for item in self.items)
    
    def save_to_file(self):

        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                for item in self.items:
                    
                    f.write(f"{item.name}|{item.quantity}|{item.price}\n")
            return True
        except Exception:
            return False
    
    def load_from_file(self):

        try:
            self.items = [] 
            with open(self.filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line: 
                        parts = line.split('|')
                        if len(parts) == 3:
                            name = parts[0]
                            quantity = int(parts[1])
                            price = int(parts[2])
                            item = WarehouseItem(name, quantity, price)
                            self.items.append(item)
            return True
        except Exception:

            self.items = []
            return False