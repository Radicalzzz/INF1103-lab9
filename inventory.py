import json
import csv

from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from supplier import Supplier
from productfactory import ProductFactory

class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def remove_product(self, product_id:str) -> None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def display_all(self) -> None:
        if not self.__products:
            print("No products in inventory.")
            return
        
        print("\nCurrent Inventory:")
        print("-------------------------------------------------------")

        for index, product in enumerate(self.__products):
            if index > 0:
                print()

            product.display_information()
            print(product.get_fulfilment_info())
            if isinstance(product, PhysicalProduct):
                print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")

        print("-------------------------------------------------------")

    def get_products(self) -> list[Product]:
        return self.__products.copy()

    def save_inventory(self) -> None:
        data = []

        for product in self.__products:
            supplier = product.get_supplier()
            product_data = {
                "id": product.get_product_id(),
                "name": product.get_product_name(),
                "price": product.get_price(),
                "stock": product.get_stock(),
                "supplier": {
                    "id": supplier.get_supplier_id(),
                    "name": supplier.get_name(),
                    "contact_email": supplier.get_contact_email()
                }
            }

            if isinstance(product, PhysicalProduct):
                product_data["type"] = "physical"
                product_data["weight"] = product.get_weight()

            elif isinstance(product, DigitalProduct):
                product_data["type"] = "digital"
                product_data["download_size"] = product.get_download_size()

            else:
                raise ValueError(f"Unsupported product type: {type(product)}")

            data.append(product_data)

        with open("inventory.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_inventory(self) -> None:
        try:
            with open("inventory.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return

        loaded_products: list[Product] = []
        suppliers: dict[str, Supplier] = {}  

        for product_data in data:
            supplier_data = product_data.get("supplier")

            if supplier_data is None:
                supplier_data ={
                    "id": "Unknown",
                    "name": "Unknown supplier",
                    "contact_email": ""
                    }

            supplier_id = supplier_data["id"]

            if supplier_id not in suppliers:
                suppliers[supplier_id] = Supplier(
                    supplier_id,
                    supplier_data["name"],
                    supplier_data["contact_email"]
                )

            supplier = suppliers[supplier_id]
            product_type = product_data.get("type")

            if product_type == "physical":
                product = PhysicalProduct(
                    product_data["id"],
                    product_data["name"],
                    product_data["price"],
                    product_data["stock"],
                    product_data["weight"],
                    supplier
                )

            elif product_type == "digital":
                product = DigitalProduct(
                    product_data["id"],
                    product_data["name"],
                    product_data["price"],
                    product_data["stock"],
                    product_data["download_size"],
                    supplier
                )

            else:
                raise ValueError(f"Unsupported product type: {product_type}")
            
            loaded_products.append(product)
            
        self.__products = loaded_products

    def load_products(self, path: str, supplier: Supplier) -> None:
        try:
            file = open(path, newline="", encoding="utf-8")
        except FileNotFoundError:
            print(f"Products file not found: {path}")

        else:
            loaded = 0
            with file:
                reader = csv.reader(file)
                next(reader, None)  # Skip the header

                for row_number, row in enumerate(reader, start=2):
                    try:
                        if len(row) != 5:
                            raise ValueError("Expected 5 columns.")

                        product = ProductFactory.create(
                            product_type=row[0],
                            product_id=row[1],
                            name=row[2],
                            price=float(row[3]),
                            stock_quantity=int(row[4]),
                            supplier=supplier
                        )

                        self.add_product(product)
                        loaded += 1

                    except ValueError as error:
                        print(f"Row {row_number} skipped: {error}")

            print(f"{loaded} products loaded.")

        finally:
            print("Load attempt finished.")