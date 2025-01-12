from src.products import Category, Product


def test_product(product_a: Product) -> None:
    """testing init Product"""

    product_dict = {
        "name": "A",
        "description": "product A",
        "price": 10.0,
        "quantity": 10,
    }
    dict_a = {
        "name": product_a.name,
        "description": product_a.description,
        "price": product_a.price,
        "quantity": product_a.quantity,
    }
    assert dict_a == product_dict


def test_category(category_a: Category, product_a: Product) -> None:
    """testing init Category"""

    dict_c = {
        "name": category_a.name,
        "description": category_a.description,
        "products": category_a.products,
    }
    category_dict = {
        "name": "C",
        "description": "category C",
        "products": [product_a]
    }
    Category.category_count -= 1
    Category.product_count -= 1
    assert dict_c == category_dict


def test_category_count(categories: list[Category]) -> None:
    """testing whether categories and products are counted correctly"""

    assert Category.category_count == 2 and Category.product_count == 4
