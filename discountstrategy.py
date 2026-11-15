from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        self.__percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)

class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        self.__threshold = threshold
        self.__amount = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total

if __name__ == "__main__":
    print(NoDiscount().apply(100))  # Output: 100
    print(PercentageDiscount(10).apply(100))  # Output: 90.0
    print(BulkDiscount(200, 20).apply(250))  # Output: 230
    print(BulkDiscount(200, 20).apply(150))  # Output: 150