from abc import ABC, abstractmethod
import math

# Создаём абстрактный базовый класс Shape, чтобы
# наследоваться от него. Также используем @abstractmethod,
# чтобы наследники реализовывали area и perimeter.

class Shape(ABC):
    @abstractmethod
    def area(self): pass

    @abstractmethod
    def perimeter(self): pass

    def compare_area(self, other): return self.area() - other.area()
    def compare_perimeter(self, other): return self.perimeter() - other.perimeter()

class Rectangle(Shape):
    def __init__(self, width, height): self.w, self.h = width, height
    def area(self): return self.w * self.h
    def perimeter(self): return 2 * (self.w + self.h)

class Square(Rectangle): # Square - частный случай Rectangle, где width == height
    def __init__(self, side): super().__init__(side, side)

class Triangle(Shape):
    def __init__(self, a, b, c): self.a, self.b, self.c = a, b, c
    def perimeter(self): return self.a + self.b + self.c
    def area(self):
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c)) # Формула Герона

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return math.pi * self.r ** 2
    def perimeter(self): return 2 * math.pi * self.r

#
# Тестируем!
#

if __name__ == "__main__":       
    c1 = Circle(3)
    s1 = Square(4)

    print("Площадь круга больше площади квадрата?" , c1.compare_area(s1) > 0)
    print("Периметр круга меньше периметра квадрата?" , c1.compare_perimeter(s1) < 0)

# Также можно добавить:
# 1) магические методы __lt__, __gt__ и др. для удобного сравнения
# 2) __repr__ для вывода подробностей при печати объектов
# 3) __str__ для форматированного красивого вывода