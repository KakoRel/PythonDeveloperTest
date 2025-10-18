import math
from abc import ABC, abstractmethod


class Shape(ABC):

    @abstractmethod
    def area(self) -> float:
        pass


class Circle(Shape):

    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Радиус должен быть положительным числом")
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2


class Triangle(Shape):

    def __init__(self, a: float, b: float, c: float):
        if any(side <= 0 for side in (a, b, c)):
            raise ValueError("Стороны треугольника должны быть положительными")
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("С указанными сторонами треугольник не существует")
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def is_right(self) -> bool:
        # Проверка является ли треугольник прямоугольным.
        sides = sorted([self.a, self.b, self.c])
        return math.isclose(sides[2] ** 2, sides[0] ** 2 + sides[1] ** 2, rel_tol=1e-9)

        
    
