# E-commerce

**products**
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
- *read_json* - the function reads a list of Categories from a json file
- *CategoryIter* - the class for get a product from a category
  - methods:
    - *get_product* - return an item from the category's products
