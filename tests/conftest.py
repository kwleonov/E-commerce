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
def category_a(product_a: Product) -> None:
    """the fixture for the test_category"""
    category = Category(name="C",
                        description="category C",
                        products=[product_a])
    return category
