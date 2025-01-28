import json
import pathlib
import sys
from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import ClassVar, TypedDict

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

NEGATIVE_ZERO_PRICE = "Цена не должна быть нулевая или отрицательная"
VALUE_ERR_MSG = "Товар с нулевым количеством не может быть добавлен"

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


class BaseProduct(ABC):
    """the abstract class as base for the Product class"""

    __slots__ = [
        "name",
        "descriptions",
        "__price",
        "quantity"
    ]

    @classmethod
    @abstractmethod
    def new_product(cls, product_dict) -> Self:
        pass


class MixinPrint:
    """the mixin class
    prints information about the object
    to the console"""

    def __repr__(self) -> str:
        """override __repr__ for print info
        to the console"""

        type_of_product = type(self)
        attrs = self.__dict__
        repr = [f"'{k}'='{v}'" for k, v in sorted(attrs.items())]
        return f"{type_of_product}({', '.join(repr)})"

    def __init__(self) -> None:
        """print repr to the console"""

        print(f"{self!r}")


class Product(BaseProduct, MixinPrint):
    """class Product
        attributes:
            name - the name of the product
            description - the description of the product
            price - the cost of the product for sale
            quantity - the quantity of the product in stock
        methods:
            new_product - the classmethod creates the product
            instance"""

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

        if quantity <= 0:
            raise ValueError(VALUE_ERR_MSG)
        self.name = name
        self.__price = price
        self.quantity = quantity
        self.description = description
        super().__init__()

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
        if price > self.__price:
            self.__price = price
            return
        if price < self.__price:
            print(f"Новая цена ({price}) ниже чем старая ({self.__price})")
            while True:
                user_answer = input("Нужно ли понизить цену? (y/n):")
                user_answer = user_answer.lower()
                print()
                if user_answer == "y":
                    self.__price = price
                    return
                if user_answer == "n":
                    return
                print("""Выберите нужный вариант нажав кнопу:
                                'y' - да, цену понижаем
                                'n' - нет, оставляем старую.""")

    @classmethod
    def new_product(cls, product_dict: Product_json) -> Self:
        """create the new product from dictionary"""

        return cls(product_dict["name"],
                   product_dict["description"],
                   product_dict["price"],
                   product_dict["quantity"])

    def __str__(self) -> str:
        """override __str__ method for return str by format:
        'Название продукта, X руб. Остаток: X шт'"""

        return f"{self.name}, {self.__price} руб, Остаток: {self.quantity} шт"

    def __add__(self, product: Self) -> float:
        """override the __add__ method to return
        the sum of multiplying the price by the quantity of each product"""
        if not isinstance(product, type(self)):
            raise TypeError
        result = self.__price * self.quantity
        result += product.price * product.quantity
        return result

    def __repr__(self) -> str:
        "override __repr__ in the MixinPrint class"

        return super().__repr__()


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
        if not isinstance(product, Product):
            raise TypeError
        if product.name in self.__product_names:
            index = self.__product_names[product.name]
            self.__products[index].quantity += product.quantity
            if product.price > self.__products[index].price:
                self.__products[index].price = product.price
            return
        index = len(self.__products)
        self.__product_names[product.name] = index
        self.__products.append(product)
        Category.product_count += 1

    def __str__(self) -> str:
        """override the __str__ method for return str by format:
        'Название категории, количество продуктов: X шт',
        где количество продуктов - общее количество товаров
        на складе (quantity) всех продуктов данной категории"""

        quantity = sum([p.quantity for p in self.__products])
        return f"{self.name}, количество продуктов: {quantity} шт"

    def __iter__(self) -> Self:
        """iterator for the __products"""
        self.__current_index = 0
        return self

    def __next__(self) -> Product:
        """get next item of the __products"""
        if self.__current_index >= len(self.__products):
            raise StopIteration
        product = self.__products[self.__current_index]
        self.__current_index += 1
        return product

    def middle_price(self) -> float:
        """return the average price of products"""

        average_price = 0.0
        try:
            quantity = sum([p.quantity for p in self.__products])
            pr = sum([p.price * p.quantity for p in self.__products])
            average_price = pr / quantity
        except ZeroDivisionError:
            return 0.0
        return average_price


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


class CategoryIter:
    """iterator for products of category"""
    def __init__(self, category: Category) -> None:
        self.__category = category

    def get_product(self) -> Generator[Product]:
        """generator for the products of the category"""
        for product in self.__category:
            yield product


class Smartphone(Product):
    """class Smartphone
        attributes:
            name - the name of the product
            description - the description of the product
            price - the cost of the product for sale
            quantity - the quantity of the product in stock
            efficiency - the efficiency of the smartphone model
            model - the name of the smartphone model
            memory - the memory that is installed in the smartphone
            color - the color of the smartphone
        methods:
            new_product - the classmethod creates the product
            instance"""

    def __init__(self, name, description, price, quantity,
                 efficiency, model, memory, color) -> None:
        """the constructor of the Smartphone class"""

        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)


class LawnGrass(Product):
    """class Smartphone
            attributes:
                name - the name of the product
                description - the description of the product
                price - the cost of the product for sale
                quantity - the quantity of the product in stock
                country - the country where lawn grass is grown
                germination_period - the germination period of the lawn grass
                color - the color of the lawn grass
            methods:
                new_product - the classmethod creates the product
                instance"""

    def __init__(self, name, description, price, quantity,
                 country, germination_period, color):
        """the constructor of the LawnGrass class"""

        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)
