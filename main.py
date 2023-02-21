import os
import requests
from woocommerce import API
from config import url_woocommerce, consumer_key, consumer_secret, url_wordpress, username_wordpress, password_wordpress
from dataclasses import dataclass


# Inicjalizacja API Woocommerce
wcapi = API(
    url=url_woocommerce,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
)

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
@dataclass
def Product():
    name: str
    description: str
    categories: list[dict]

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
