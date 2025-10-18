from geometry import *

circle = Circle(5)
triangle = Triangle(3, 4, 5)

print("Площадь круга:", calculate_area(circle)) #78.53
print("Площадь треугольника:", calculate_area(triangle)) #6
print("Треугольник прямоугольный?", triangle.is_right()) #True
