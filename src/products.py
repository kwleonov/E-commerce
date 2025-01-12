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
