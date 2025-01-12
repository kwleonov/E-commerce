import pytest

from src.products import Category, Product


@pytest.fixture
def product_a() -> Product:
    """the fixture for the test_product and the test_category"""
    product = Product(name="A",
                      description="product A",
                      price=10.0,
                      quantity=10)
    return product


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
