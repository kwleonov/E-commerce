from unittest.mock import patch

from src.products import Category, Product, read_json


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
    category_dict = {"name": "C", "description": "category C",
                     "products": [product_a]}
    Category.category_count -= 1
    Category.product_count -= 1
    assert dict_c == category_dict


def test_category_count(categories: list[Category]) -> None:
    """testing whether categories and products are counted correctly"""

    assert Category.category_count == 2 and Category.product_count == 4


def test_json_not_exist_read() -> None:
    """testing for open a not exist json file"""
    categories = read_json("data/notexist.json")
    assert len(categories) == 0


def test_read_json() -> None:
    """testing the correctness the read_json"""

    json_data = """[{
            "name": "A", "description": "category A",
            "products": [
                {
                    "name": "A1",
                    "description": "product A1",
                    "price": 10.0,
                    "quantity": 2
                }
            ]
        }]"""
    categories = [
        Category(
            name="A",
            description="category A",
            products=[
                Product(name="A1", description="product A1",
                        price=10.0, quantity=2),
            ],
        )
    ]
    with patch("builtins.open") as mock_open:
        mock_json = mock_open.return_value.__enter__.return_value
        mock_json.read.return_value = json_data
        categories_json = read_json("data/products.json")
        assert len(categories_json) == len(categories)
        for i in range(len(categories)):
            c1 = categories[i]
            c2 = categories_json[i]
            assert c1.name == c2.name
            assert c1.description == c2.description
            assert len(c1.products) == len(c2.products)
            for j in range(len(c1.products)):
                p1 = c1.products[j]
                p2 = c2.products[j]
                assert p1.name == p2.name
                assert p1.description == p2.description
                assert p1.price == p2.price
                assert p1.quantity == p2.quantity


def test_read_json_error() -> None:
    """testing for bad json data"""

    json_data = """[{
                'name': 'A', 'description': 'category A',
                'products': [
                    {
                        'name': 'A1',
                        'description': 'product A1',
                        'price': 10.0,
                        'quantity': 2
                    }
                ]
            }]"""
    with patch("builtins.open") as mock_open:
        mock_json = mock_open.return_value.__enter__.return_value
        mock_json.read.return_value = json_data
        categories_json = read_json("data/products.json")
        assert len(categories_json) == 0
