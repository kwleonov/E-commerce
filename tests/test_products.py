from typing import Any
from unittest.mock import patch

from pytest import CaptureFixture

from src.products import NEGATIVE_ZERO_PRICE, Category, Product, read_json


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


def test_price_setter(product_a: Product,
                      capsys: CaptureFixture[Any]) -> None:
    """testing the price setter"""
    price = product_a.price + 10
    product_a.price = price
    assert product_a.price == price
    product_a.price = -110.0
    assert product_a.price == price
    captured = capsys.readouterr()
    assert captured.out.strip() == NEGATIVE_ZERO_PRICE
    price -= 10
    with patch("builtins.input") as mock_input:
        mock_input.return_value = "n"
        product_a.price = price
        captured = capsys.readouterr()
        assert captured.out.strip()[:10] == "Новая цена"
        assert product_a.price > price
    with patch("builtins.input") as mock_input:
        mock_input.return_value = "y"
        product_a.price = price
        captured = capsys.readouterr()
        assert captured.out.strip()[:10] == "Новая цена"
        assert product_a.price == price
    with patch("builtins.input") as mock_input:
        product_a.price += 10
        mock_input.side_effect = ["w", "y"]
        product_a.price = price
        captured = capsys.readouterr()
        assert captured.out.strip()[-22:] == "нет, оставляем старую."
        assert product_a.price == price


def test_category(category_a: Category, product_a: Product) -> None:
    """testing init Category"""

    dict_a = {
        "name": category_a.name,
        "description": category_a.description,
        "products": category_a.products,
    }
    category_b = Category("C", "category C", [product_a])
    dict_b = {
        "name": category_b.name,
        "description": category_b.description,
        "products": category_b.products,
    }
    assert dict_a == dict_b


def test_category_count(categories: list[Category]) -> None:
    """testing whether categories and products are counted correctly"""

    category_count = Category.category_count
    product_count = Category.product_count
    new_category = Category(
        "New", "new category", [Product("New", "new product", 1.0, 1)]
    )
    category_count += 1
    product_count += 1
    assert Category.category_count == category_count
    assert Category.product_count == product_count
    new_category.add_product(
        Product.new_product({
            "name": "Another",
            "description": "another product",
            "price": 2.0,
            "quantity": 2}))
    product_count += 1
    assert Category.category_count == category_count
    assert Category.product_count == product_count


def test_add_product(product_a: Product, category_a: Category) -> None:
    """testing add the exist product"""
    product_count = Category.product_count
    quantity = product_a.quantity
    price = product_a.price
    new_product = Product.new_product({
        "name": product_a.name,
        "description": product_a.description,
        "price": product_a.price / 2,
        "quantity": 10
    })
    category_a.add_product(new_product)
    assert Category.product_count == product_count
    assert product_a.quantity == quantity + new_product.quantity
    assert product_a.price == price
    new_product.price = product_a.price * 2
    quantity = product_a.quantity
    category_a.add_product(new_product)
    assert Category.product_count == product_count
    assert product_a.quantity == quantity + new_product.quantity
    assert product_a.price == new_product.price


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
            assert c1.products == c2.products


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
