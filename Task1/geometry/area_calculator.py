from .shapes import Shape

    # Универсальная функция вычисления площади фигуры без знания её типа.
    # Принимает объект, реализующий метод .area().
def calculate_area(shape: Shape) -> float:

    if not isinstance(shape, Shape):
        raise TypeError("Аргумент должен быть экземпляром класса Shape")
    return shape.area()
