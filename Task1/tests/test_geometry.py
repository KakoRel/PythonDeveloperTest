import math
import pytest
from geometry import Circle, Triangle, calculate_area

def test_circle_area():
    circle = Circle(1)
    assert math.isclose(circle.area(), math.pi, rel_tol=1e-9)


def test_triangle_area():
    triangle = Triangle(3, 4, 5)
    assert math.isclose(triangle.area(), 6.0, rel_tol=1e-9)


def test_right_triangle():
    triangle = Triangle(3, 4, 5)
    assert triangle.is_right() is True


def test_non_right_triangle():
    triangle = Triangle(2, 3, 4)
    assert triangle.is_right() is False


def test_calculate_area_dynamic():
    # Проверка вычисления без знания типа фигуры
    circle = Circle(2)
    triangle = Triangle(3, 4, 5)
    assert math.isclose(calculate_area(circle), math.pi * 4, rel_tol=1e-9)
    assert math.isclose(calculate_area(triangle), 6.0, rel_tol=1e-9)


def test_invalid_circle():
    import pytest
    with pytest.raises(ValueError):
        Circle(-1)


def test_invalid_triangle():
    with pytest.raises(ValueError):
        Triangle(1, 2, 3)
