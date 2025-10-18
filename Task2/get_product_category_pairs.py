from pyspark.sql import DataFrame

def get_product_category_pairs(
    products: DataFrame,
    categories: DataFrame,
    product_category: DataFrame
) -> DataFrame:
    """
    Возвращает DataFrame с парами (product_name, category_name),
    включая продукты без категорий (category_name = None).
    """
    # Соединяем продукты со связями
    joined = products.join(
        product_category,
        products.id == product_category.product_id,
        how="left"
    ).join(
        categories,
        product_category.category_id == categories.id,
        how="left"
    )

    # Выбираем только имена
    result = joined.select(
        products["name"].alias("product_name"),
        categories["name"].alias("category_name")
    )

    return result
