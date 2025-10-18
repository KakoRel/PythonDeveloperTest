import findspark
findspark.init()

from pyspark.sql import SparkSession
from get_product_category_pairs import get_product_category_pairs

spark = SparkSession.builder.appName("SimpleTest").getOrCreate()

def calculate_product_category_pairs():
    # Простые тестовые данные в виде списков
    products = spark.createDataFrame([
        (1, "Ноутбук"),
        (2, "Мышь"), 
        (3, "Клавиатура"),
        (4, "Наушники")
    ], ["id", "name"])

    categories = spark.createDataFrame([
        (1, "Электроника"),
        (2, "Компьютерная техника"),
        (3, "Периферия")
    ], ["id", "name"])

    product_category = spark.createDataFrame([
        (1, 1),  # Ноутбук -> Электроника
        (1, 2),  # Ноутбук -> Компьютерная техника
        (2, 2),  # Мышь -> Компьютерная техника
        (2, 3),  # Мышь -> Периферия
        (3, 3),  # Клавиатура -> Периферия
        # Наушники без категорий
    ], ["product_id", "category_id"])

    print("=== ИСХОДНЫЕ ДАННЫЕ ===")
    print("Продукты:")
    products.show()
    print("Категории:")
    categories.show()
    print("Связи продукт-категория:")
    product_category.show()

    # Запускаем нашу функцию
    result = get_product_category_pairs(products, categories, product_category)

    print("=== РЕЗУЛЬТАТ ===")
    result.show()

if __name__ == "__main__":
    calculate_product_category_pairs()
    spark.stop()