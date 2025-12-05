class Drink:
    def __init__(self, name, type, cost, volume):
        self.name = name
        self.type = type
        self.cost = cost
        self.volume = volume
        
    def show_info(self):
        return f"Информация о напитках: {self.name} {self.type} {self.cost} {self.volume}"
    def change_cost(self):
        pass
    
capuccino = Drink('Капучино', 'кофе', 200, 'M')

class Order:
    def __init__(self, number, list, client, status, endCost):
        self.number = number
        self.list = list
        self.client = client
        self.status = status
        self.endCost = endCost
        
    def add_drink(self, list):
        self.list = Drink.show_info()
        


capuccino = Drink('Капучино', 'кофе', 200, 'M')
matcha = Drink('Матча', 'чай', 300, 'M')

print(Order.add_drink)