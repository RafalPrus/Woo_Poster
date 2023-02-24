import os
import requests
from woocommerce import API
from config import url_woocommerce, consumer_key, consumer_secret, url_wordpress, username_wordpress, password_wordpress
from dataclasses import dataclass


# Inicjalizacja API Woocommerce


# dane produktu
product_data = {
    "name": "Ultimate 2",
    "description": "Opis testowego produktu",
    "categories": [
        {
            "id": 711
        },
{
            "id": 33
        }
    ]
}

class Application():
    WCAPI = API(
        url=url_woocommerce,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
    )

    def add_product(self, product_details: dict) -> str:
        response = self.WCAPI.post("products", product_details).json()
        product_id = response.get('id')
        return product_id

@dataclass
class Product():
    _name: str
    _description: str
    _categories: list[dict]

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, product_name: str):
        self._name = product_name

    @property
    def description(self) -> str:
        return self._description

    @name.setter
    def description(self, product_description: str):
        self._description = product_description

    @property
    def categories(self) -> list[dict]:
        return self._categories

    @name.setter
    def description(self, category_list: list[dict]):
        self._categories = category_list

    def set_export_details(self):
        export = {
            "name": self._name,
            "description": self._description,
            "categories": self._categories
        }

        return export


# dodawanie produktu do sklepu
response = wcapi.post("products", product_data).json()
product_id = response.get('id')

os.chdir('products')
current_path = os.getcwd()
image_folder = current_path
images_ids = []
for file_name in os.listdir(image_folder):
    if file_name.endswith(".jpg"):
        file_path = os.path.join(image_folder, file_name)

        # Otwórz plik ze zdjęciem i przeczytaj jego zawartość
        with open(file_name, "rb") as image_file:
            image_data = image_file.read()

        # Wyślij zapytanie POST z danymi autoryzacyjnymi i danymi pliku
        response = requests.post(
            url_wordpress,
            auth=(username_wordpress, password_wordpress),
            files={"file": (file_name, image_data)}
        )

        # Wyświetl odpowiedź serwera
        print(response.json())
        image_id = response.json().get("id")
        print(image_id)
        if response.status_code == 201:
            image_id = response.json().get("id")
            images_ids.append(image_id)
        else:
            print(response.status_code)
            print(response)
print(images_ids)
print([{"id": image_id} for image_id in images_ids])
wcapi.post("products/%d" % product_id, {"images": [{"id": image_id} for image_id in images_ids]})
