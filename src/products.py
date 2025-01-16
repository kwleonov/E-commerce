import json
import pathlib
import sys
from typing import ClassVar, TypedDict

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

NEGATIVE_ZERO_PRICE = "Цена не должна быть нулевой или отрицательная"

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
    __price: float = 0.0
    quantity: int = 0

    def __init__(self,
                 name: str,
                 description: str,
                 price: float,
                 quantity: int):
        """constructor for the Product class.
        Init the name, description, price and quantity attributes"""

        self.name = name
        self.__price = price
        self.quantity = quantity
        self.description = description

    @property
    def price(self) -> float:
        """returns the value of the __price attribute"""
        return self.__price

    @price.setter
    def price(self, price: float) -> None:
        """set the value of the __price attribute"""
        if price <= 0:
            print(NEGATIVE_ZERO_PRICE)
            return
        self.__price = price

    @classmethod
    def new_product(cls, product_dict: Product_json) -> Self:
        """create the new product from dictionary"""

        return cls(product_dict["name"],
                   product_dict["description"],
                   product_dict["price"],
                   product_dict["quantity"])


class Category:
    """class Category
        attributes:
            name - the name of the category
            description - the description of the category
            products - the list of the products"""

    name: str = ""
    description: str = ""
    __products: list[Product] = []
    __product_names: dict[str, int] = dict()
    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    def __init__(self,
                 name: str,
                 description: str,
                 products: list[Product]) -> None:
        """constructor for the Category class.
        Init the name, description and products attributes"""

        self.name = name
        self.description = description
        self.__products = products
        self.__product_names = {v.name: i for i, v in enumerate(products)}
        Category.category_count += 1
        Category.product_count += len(products)

    @property
    def products(self) -> str:
        """returns str by format:
        f'{name}, {price} руб. Остаток: {quantity} шт.\n'"""
        products_str = "".join(
            [f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт.\n"
             for p in self.__products]
        )
        return products_str

    def add_product(self, product: Product) -> None:
        """add the product to the __products list of the Category's instance"""
        if product.name in self.__product_names:
            index = self.__product_names[product.name]
            self.__products[index].quantity += product.quantity
            if product.price > self.__products[index].price:
                self.__products[index].price = product.price
            return
        self.__products.append(product)
        Category.product_count += 1


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
