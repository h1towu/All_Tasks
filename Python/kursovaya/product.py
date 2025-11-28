class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"{self.name} - {self.price} руб. (осталось: {self.quantity})"