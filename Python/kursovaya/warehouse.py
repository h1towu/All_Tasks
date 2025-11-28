import json
from product import Product  # Добавляем импорт

class Warehouse:
    def __init__(self):
        self.products = []
        self.next_id = 1
    
    def add_product(self, name, price, quantity):
        product = Product(self.next_id, name, price, quantity)
        self.products.append(product)
        self.next_id += 1
        return product
    
    def remove_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                self.products.remove(product)
                return True
        return False
    
    def find_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None
    
    def update_quantity(self, product_id, new_quantity):
        product = self.find_product(product_id)
        if product:
            product.quantity = new_quantity
            return True
        return False
    
    def get_all_products(self):
        return self.products
    
    def save_to_file(self):
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
    
    def load_from_file(self):
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
            return True
        except:
            return False