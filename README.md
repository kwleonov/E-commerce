# E-commerce

**products**
- *BaseProduct* - the abstract class for products
- *MixinPrint* - the base class for the Product class,
prints information about the object to the console
- *Product* - class Product
  - attributes:
    - *name* - the name of the product
    - *description* - the description of the product
    - *price* - the cost of the product for sale
    - *quantity* - the quantity of the product in stock
  - methods:
    - *new_product* - create a new product from dictionary
- *Category* - class Category
  - attributes:
    - *name* - the name of the category
    - *description* - the description of the category
    - *products* - the list of the products as the str by format:  
      f'{name}, {price} руб. Остаток: {quantity} шт.\n'
    - *category_count* - the class attribute is count of categories
    - *product_count* - the class attribute is count of products
  - methods:
    - *add_product* - add the product to list of Category's products
    - *middle_price* - return the average price of Category's products
- *read_json* - the function reads a list of Categories from a json file
- *CategoryIter* - the class for get a product from a category
  - methods:
    - *get_product* - the generator returns an item from 
    the Category's products
- *Smartphone* - class Smartphone
  - attributes:
    - *name* - the name of the product
    - *description* - the description of the product
    - *price* - the cost of the product for sale
    - *quantity* - the quantity of the product in stock
    - *efficiency* - the efficiency of the smartphone model
    - *model* - the name of the smartphone model
    - *memory* - the memory that is installed in the smartphone
    - *color* - the color of the smartphone
  - methods:
    - *new_product* - create a new product from dictionary
- *LawnGrass* - class LawnGrass
  - attributes:
      - *name* - the name of the product
      - *description* - the description of the product
      - *price* - the cost of the product for sale
      - *quantity* - the quantity of the product in stock
      - *country* - the country where lawn grass is grown
      - *germination_period* - the germination period of the lawn grass
      - *color* - the color of the lawn grass
  - methods:
    - new_product - create a new product from dictionary
