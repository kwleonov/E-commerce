import pytest

from src.products import Category, Product, Product_json


@pytest.fixture
def product_a() -> Product:
    """the fixture for the test_product and the test_category"""
    product = Product(name="A",
                      description="product A",
                      price=10.0,
                      quantity=10)
    return product


@pytest.fixture
def product_b() -> Product:
    """the fixture for the test_product_add"""
    product: Product_json = {
        "name": "B",
        "description": "product B",
        "price": 20.0,
        "quantity": 3
    }
    return Product.new_product(product)


@pytest.fixture()
def category_a(product_a: Product) -> Category:
    """the fixture for the test_category"""
    category = Category(name="C",
                        description="category C",
                        products=[product_a])
    return category


@pytest.fixture
def categories() -> list[Category]:
    """the fixture of the list by Category
    returns a list of 2 categories with 4 products"""

    products_a = [Product(name="A1",
                          description="product A",
                          price=10.0,
                          quantity=10),
                  Product(name="A2",
                          description="product A",
                          price=10.0,
                          quantity=10)]
    products_b = [Product(name="B1",
                          description="product B",
                          price=10.0,
                          quantity=5),
                  Product(name="B2",
                          description="product B",
                          price=10.0,
                          quantity=20)]
    return [
        Category(name="A", description="category A", products=products_a),
        Category(name="B", description="category B", products=products_b),
    ]


@pytest.fixture
def smartphone_dict():
    """the fixture for testing the Smartphone class and adding with
    the LawnGrass object"""
    return {
        "name": "the Brand's smartphone",
        "description": "the smartphone from a famous brand",
        "price": 111_111.99,
        "quantity": 99,
        "efficiency": 0.99,
        "model": "the newest model",
        "memory": 512,
        "color": "gold"
    }


@pytest.fixture
def lawngrass_dict():
    """the fixture for testing the LawnGrass class and adding with
    the Smartphone object"""
    return {
        "name": "the Brand's lawn grass",
        "description": "the lawn grass from a famous Belgian brand",
        "price": 111.99,
        "quantity": 99,
        "country": "Belgium",
        "germination_period": "60 days",
        "color": "dark green"
    }
