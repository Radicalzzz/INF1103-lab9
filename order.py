from orderline import OrderLine
from product import Product
from discountstrategy import DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount

class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount = NoDiscount() if discount is None else discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines.copy()

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount
