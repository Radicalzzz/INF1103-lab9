from discountstrategy import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount
from order import Order
from supplier import Supplier
from physicalproduct import PhysicalProduct
from productfactory import ProductFactory
from orderline import OrderLine

print(NoDiscount().apply(100))  # Output: 100
print(PercentageDiscount(10).apply(100))  # Output: 90
print(BulkDiscount(250, 10).apply(150))  # Output: 150

supplier = Supplier("S001", "Supplier A", "contact@abc.com")
product = PhysicalProduct("P001", "Product A", 125.00, 10, 1.0, supplier)
order = Order("O001", BulkDiscount(200, 20))
order.add_order_line(product,2)
print(f"Bulk discount total: {order.calculate_total():.2f}") # Output: 230.00
order.set_discount(PercentageDiscount(10))
print(f"Percentage discount total: {order.calculate_total():.2f}") # Output: 225.00

order.set_discount(StudentDiscount())
print(f"Student discount total: {order.calculate_total():.2f}") # Output: 237.50

keyboard = ProductFactory.create("physical", "P010", "Mechanical Keyboard", 80.0, 50, supplier, weight=1.2)
ebook = ProductFactory.create("digital", "D010", "Python Programming", 20.0, 100, supplier, download_size=5.0)

for product in [keyboard, ebook]:
    product.display_information()
    print(product.get_fulfilment_info())
    print()

try:
    ProductFactory.create("physical", "P100", "Invalid Product", 0.0, 10, supplier, weight=1.0)

except ValueError as error:
    print(error)

try:
    keyboard.update_stock(-5)

except ValueError as error:
    print(error)

try:
    OrderLine(keyboard, 0)

except ValueError as error:
    print(error)
