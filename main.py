import os
import requests
from woocommerce import API
from config import url_woocommerce, consumer_key, consumer_secret, url_wordpress, username_wordpress, password_wordpress
from dataclasses import dataclass


# Inicjalizacja API Woocommerce




class Application():
    WCAPI = API(
        url=url_woocommerce,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
    )



    def main(self):
        self.scan_product_folder()


    def add_product(self, new_product) -> None:
        product_details = new_product.set_export_details()
        response = self.WCAPI.post("products", product_details).json()
        product_id = response.get('id')
        print('ID PRODUCKTU')
        print(product_id)
        new_product.product_id = product_id


    def scan_product_folder(self):
        os.chdir('products')
        products_folder = os.getcwd()
        for product_name in os.listdir(products_folder):
            if self.check_thumbnails_exists(product_name) and self.check_product_info_exists(product_name):
                print('skanowanie folderow')
                print(f'sciezka: {os.getcwd()}')
                new_product = Product()
                self.get_info(product_name, new_product)
                self.add_images(product_name, new_product)
                print('rozpoczynam dodawanie produktu...')
                self.add_product(new_product)
                print('rozpoczynam dodawanie zdjec do produktu...')
                self.add_images_to_product(new_product)



    def check_thumbnails_exists(self, product_name):
        print('w skanowanie folderow')
        os.chdir(product_name)
        product_folder = os.getcwd()
        if 'small' in os.listdir(product_folder):
            os.chdir('..')
            return True
        else:
            os.chdir('..')
            return False

    def check_product_info_exists(self, product_name):
        os.chdir(product_name)
        product_folder = os.getcwd()
        if 'info.txt' in os.listdir(product_folder):
            os.chdir('..')
            return True
        else:
            os.chdir('..')
            return False


    def add_images(self, product_name, new_product):
        os.chdir(product_name)
        os.chdir('small')
        images_folder = os.getcwd()
        for file_name in os.listdir(images_folder):
            if file_name.endswith(".jpg"):
                file_path = os.path.join(images_folder, file_name)

                # Otwórz plik ze zdjęciem i przeczytaj jego zawartość
                with open(file_name, "rb") as image_file:
                    image_data = image_file.read()

                # Wyślij zapytanie POST z danymi autoryzacyjnymi i danymi pliku
                response = requests.post(
                    url_wordpress,
                    auth=(username_wordpress, password_wordpress),
                    files={"file": (file_name, image_data)}
                )

                image_id = response.json().get("id")

                if response.status_code == 201:
                    print(response.status_code)
                    print(response)
                    image_id = response.json().get("id")
                    new_product.add_id(image_id)
                else:
                    print(response.status_code)
                    print(response)
        os.chdir('..')

    def add_images_to_product(self, product):
        images_id = product.get_images_id
        product_id = product.product_id
        self.WCAPI.post("products/%d" % product_id, {"images": [{"id": image_id} for image_id in images_id]})

    def get_info(self, product_name: str, new_product, info_file='info.txt'):
        os.chdir(product_name)
        with open(info_file) as info:
            full_info = info.readlines()
            new_product.name = full_info[2]
            new_product.description = ' '.join(full_info[2:])
            categories = []
            for cat in full_info[0].split(' '):
                categories.append({'id': int(cat) })
            new_product.categories = categories
        os.chdir('..')


class Product():
    def __init__(self, name='', descripton='', categories=None, product_id=''):
        self._name = name
        self._description = descripton
        self._categories = categories
        self._product_id = product_id
        self._images_id = []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, product_name: str):
        self._name = product_name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, product_description: str):
        self._description = product_description

    @property
    def categories(self) -> list[dict]:
        return self._categories

    @categories.setter
    def categories(self, category_list: list[dict]):
        self._categories = category_list


    @property
    def product_id(self) -> str:
        return self._product_id

    @product_id.setter
    def product_id(self, id: str):
        self._product_id = id


    @property
    def get_images_id(self) -> list:
        return self._images_id


    def add_id(self, id: str):
        print(self.get_images_id)
        self._images_id.append(id)

    def set_export_details(self):
        export = {
            "name": self._name,
            "description": self._description,
            "categories": self._categories
        }

        return export


if __name__ == '__main__':
    app = Application()
    app.main()


