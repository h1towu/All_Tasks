'''
КЛАСС 1: Фрукт (Fruit)
Каждый фрукт — это просто объект с:
1. Названием ("яблоко", "банан", "апельсин")
2. Цветом
3. Ценой за 1 кг
4. Весом (сколько взял покупатель)

Что умеет фрукт:
1. Показывать информацию о себе
2. Считать стоимость: цена x вес


КЛАСС 2: Покупатель (Customer)
Каждый покупатель:
1. Имя
2. Сумма денег
3. Список купленных фруктов

Что умеет покупатель
1. Купить фрукт (добавить в список)
2. Посчитать общую сумму покупки
3. Показать, что купил
'''

class Fruit:
    def __init__(self, name, color, cost_by_kg, weight):
        self.name = name
        self.color = color
        self.cost_by_kg = cost_by_kg
        self.weight = weight
    
    def show_info(self):
        return f'{self.name} {self.color} {self.cost_by_kg} {self.weight}'
    
    def cost(self):
        return self.cost_by_kg * self.weight
    
class Buyer:
    def __init__(self, name, money, fruits):
        self.name = name
        self.money = money
        self.fruits = fruits
    
    def buy(self, fruit):
        self.fruits.append(fruit)

    def sum(self):
        sum = 0
        for fruit in self.fruits:
            sum += fruit.cost()
        return sum
    def show_info(self):
        return f'{self.name} {self.money} {self.fruits}'

fruit1 = Fruit('яблоко', 'красный', 5, '1кг')
print(fruit1.show_info())

buyer1 = Buyer('Егор', 50, [])
print(buyer1.show_info())

buyer1.buy(fruit1)

print(buyer1.show_info())
print(buyer1.sum())
