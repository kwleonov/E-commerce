import json
import pathlib
from typing import TypedDict

Product_json = TypedDict("Product_json", {
    "name": str,
    "description": str,
    "price": float,
    "quantity": int,
})


Category_json = TypedDict("Category_json", {
    "name": str,
    "description": str,
    "products": list[Product_json],
})


class Product:
    """class Product
        attributes:
            name - the name of the product
            description - the description of the product
            price - the cost of the product for sale
            quantity - the quantity of the product in stock"""

    name: str = ""
    description: str = ""
    price: float = 0.0
    quantity: int = 0

    def __init__(self,
                 name: str,
                 description: str,
                 price: float,
                 quantity: int):
        """constructor for the Product class.
        Init the name, description, price and quantity attributes"""

        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description


class Category:
    """class Category
        attributes:
            name - the name of the category
            description - the description of the category
            products - the list of the products"""

    name: str = ""
    description: str = ""
    products: list[Product] = []
    category_count: int = 0
    product_count: int = 0

    def __init__(self,
                 name: str,
                 description: str,
                 products: list[Product]) -> None:
        """constructor for the Category class.
        Init the name, description and products attributes"""

        self.name = name
        self.description = description
        self.products = products
        Category.category_count += 1
        Category.product_count += len(products)


def read_json(filename: str) -> list[Category]:
    """receives data from an Json file and returns
    list of Category"""

    categories: list[Category] = []
    categories_json: list[Category_json] = []
    if not pathlib.Path(filename).exists():
        return []
    try:
        with open(filename, encoding="utf-8") as f:
            categories_json = json.load(f)
    except json.JSONDecodeError:
        return []
    for category in categories_json:
        products: list[Product] = []
        for product in category["products"]:
            products.append(Product(
                name=product["name"],
                description=product["description"],
                price=product["price"],
                quantity=product["quantity"]
            ))
        categories.append(Category(
            name=category["name"],
            description=category["description"],
            products=products
        ))
    return categories
