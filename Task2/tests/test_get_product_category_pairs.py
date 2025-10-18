import findspark
findspark.init()

import pytest
from pyspark.sql import SparkSession, Row
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

from get_product_category_pairs import get_product_category_pairs


@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("geometry-tests").getOrCreate()


def test_basic_case(spark):
    """Базовый случай: у некоторых продуктов есть категории, у некоторых — нет"""
    products = spark.createDataFrame([
        (1, "Молоко"),
        (2, "Хлеб"),
        (3, "Яблоко"),
        (4, "Сыр"),
    ], ["id", "name"])

    categories = spark.createDataFrame([
        (10, "Молочные"),
        (11, "Фрукты"),
        (12, "Выпечка")
    ], ["id", "name"])

    product_category = spark.createDataFrame([
        (1, 10),   # Молоко → Молочные
        (2, 12),   # Хлеб → Выпечка
        (3, 11),   # Яблоко → Фрукты
        (1, 12)    # Молоко → Выпечка
    ], ["product_id", "category_id"])

    result = get_product_category_pairs(products, categories, product_category)

    expected = [
        Row(product_name="Сыр", category_name=None),
        Row(product_name="Яблоко", category_name="Фрукты"),
        Row(product_name="Хлеб", category_name="Выпечка"),
        Row(product_name="Молоко", category_name="Выпечка"),
        Row(product_name="Молоко", category_name="Молочные"),
    ]

    assert set(result.collect()) == set(expected)


def test_no_categories(spark):
    """Все продукты без категорий"""
    products_schema = StructType([
        StructField("id", IntegerType(), False),
        StructField("name", StringType(), False),
    ])
    products = spark.createDataFrame([
        (1, "Молоко"),
        (2, "Хлеб")
    ], schema=products_schema)

    categories_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])
    categories = spark.createDataFrame([], schema=categories_schema)

    product_category_schema = StructType([
        StructField("product_id", IntegerType(), True),
        StructField("category_id", IntegerType(), True)
    ])
    product_category = spark.createDataFrame([], schema=product_category_schema)

    result = get_product_category_pairs(products, categories, product_category)
    rows = result.collect()

    assert len(rows) == 2
    assert all(r.category_name is None for r in rows)


def test_multiple_products_same_category(spark):
    """Несколько продуктов в одной категории"""
    products = spark.createDataFrame([
        (1, "Молоко"),
        (2, "Сыр"),
        (3, "Йогурт")
    ], ["id", "name"])

    categories = spark.createDataFrame([
        (10, "Молочные")
    ], ["id", "name"])

    product_category = spark.createDataFrame([
        (1, 10),
        (2, 10),
        (3, 10)
    ], ["product_id", "category_id"])

    result = get_product_category_pairs(products, categories, product_category)
    names = [r.product_name for r in result.collect()]

    assert set(names) == {"Молоко", "Сыр", "Йогурт"}
    assert result.filter(F.col("category_name").isNull()).count() == 0


def test_duplicate_links(spark):
    """Дубликаты связей не должны ломать результат"""
    products = spark.createDataFrame([
        (1, "Хлеб")
    ], ["id", "name"])

    categories = spark.createDataFrame([
        (10, "Выпечка")
    ], ["id", "name"])

    product_category = spark.createDataFrame([
        (1, 10),
        (1, 10)  # повтор
    ], ["product_id", "category_id"])

    result = get_product_category_pairs(products, categories, product_category)

    # Проверяем, что дубликаты сохраняются — либо можно добавить .distinct()
    assert result.filter(F.col("product_name") == "Хлеб").count() == 2


def test_empty_all(spark):
    """Все таблицы пустые"""
    products_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])
    categories_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])
    product_category_schema = StructType([
        StructField("product_id", IntegerType(), True),
        StructField("category_id", IntegerType(), True)
    ])

    products = spark.createDataFrame([], schema=products_schema)
    categories = spark.createDataFrame([], schema=categories_schema)
    product_category = spark.createDataFrame([], schema=product_category_schema)

    result = get_product_category_pairs(products, categories, product_category)
    assert result.count() == 0

def test_category_without_products(spark):
    """Есть категории, но нет продуктов, связанных с ними"""
    products_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])
    categories_schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])
    product_category_schema = StructType([
        StructField("product_id", IntegerType(), True),
        StructField("category_id", IntegerType(), True)
    ])

    products = spark.createDataFrame([(1, "Хлеб")], schema=products_schema)
    categories = spark.createDataFrame([
        (10, "Фрукты"),
        (11, "Молочные")
    ], schema=categories_schema)
    product_category = spark.createDataFrame([], schema=product_category_schema)

    result = get_product_category_pairs(products, categories, product_category)
    data = result.collect()

    assert len(data) == 1
    assert data[0].category_name is None