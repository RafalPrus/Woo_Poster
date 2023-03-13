import os
import requests
from woocommerce import API
from config import url_woocommerce, consumer_key, consumer_secret, url_wordpress, username_wordpress, password_wordpress
from views import MainMenu, ValidatorScreen, MainAppScreen, Report


class Application:
    WCAPI = API(
        url=url_woocommerce,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
    )

    FINISHED = []
    UNFINISHED = []

    def main(self):
        while True:
            menu = MainMenu()
            screen = menu.get_screen()
            if isinstance(screen, ValidatorScreen):
                Products_Validator()
            elif isinstance(screen, MainAppScreen):
                self.scan_product_folder()
                self.print_report()
            elif isinstance(screen, Report):
                screen.print_report_menu()
            else:
                print("See you next time!!!!!!")
                return False

    def add_product(self, new_product) -> None:
        product_details = new_product.set_export_details()
        response = self.WCAPI.post("products", product_details).json()
        product_id = response.get('id')
        print('ID PRODUKTU')
        print(product_id)
        new_product.product_id = product_id


    def print_report(self):
        print('----------------------')
        print(f'Pomyślnie dodano: ')
        for num, name in enumerate(Application.FINISHED, 1):
            print(f'{num}.: {name}')
        print('----------------------')
        print(f'Nie dodano z powodu braków w plikach: ')
        for num, name in enumerate(Application.UNFINISHED):
            print(f'{num}.: {name}')


    def scan_product_folder(self, products_folder: str = 'products'):
        products_folder = Application.change_directory(products_folder)
        for product_name in os.listdir(products_folder):
            if self.check_thumbnails_exists(product_name) and self.check_product_info_exists(product_name):
                try:
                    new_product = Product()
                    self.get_info(product_name, new_product) # Update class Product with infromations from info.txt file
                    self.add_images(product_name, new_product)
                    self.add_product(new_product)
                    self.add_images_to_product(new_product)
                    Application.FINISHED.append(new_product.name.strip()) # Add product name to finished list
                    os.chdir('..')
                except:
                    if new_product:
                        Application.UNFINISHED.append(new_product.name.strip())
                    else:
                        Application.UNFINISHED.append('Unknown')
            else:
                Application.UNFINISHED.append(product_name)



    # check if folder with thumbnails exist
    def check_thumbnails_exists(self, product_name) -> bool:
        print(os.getcwd())
        product_folder = Application.change_directory(product_name)
        if 'small' in os.listdir(product_folder):
            os.chdir('..')
            return True
        else:
            os.chdir('..')
            return False

    # check if file info.txt - with product information - exist
    def check_product_info_exists(self, product_name) -> bool:
        product_folder = Application.change_directory(product_name)
        if 'info.txt' in os.listdir(product_folder):
            os.chdir('..')
            return True
        else:
            os.chdir('..')
            return False


    def add_images(self, product_name, new_product):
        os.chdir(product_name)
        images_folder = Application.change_directory('small')
        for file_name in os.listdir(images_folder):
            if file_name.endswith(".jpg"):
                # Open file with image
                with open(file_name, "rb") as image_file:
                    image_data = image_file.read()

                # Send POST request with authorization data and file data
                response = requests.post(
                    url_wordpress,
                    auth=(username_wordpress, password_wordpress),
                    files={"file": (file_name, image_data)}
                )

                self.read_response(response, new_product)
        os.chdir('..')
    @staticmethod
    def change_directory(directory_name: str):
        os.chdir(directory_name)
        curr_directory = os.getcwd()
        return curr_directory


    def read_response(self, response, product):
        if response.status_code == 201:
            image_id = response.json().get("id")
            product.add_id(image_id)
        else:
            print(response.status_code)
            print(response)

    def add_images_to_product(self, product):
        images_id = product.get_images_id
        product_id = product.product_id
        self.WCAPI.post("products/%d" % product_id, {"images": [{"id": image_id} for image_id in images_id]})

    def get_info(self, product_name: str, new_product, info_file='info.txt'):
        os.chdir(product_name)
        with open(info_file, encoding='UTF8') as info:
            full_info = info.readlines()
            new_product.name = full_info[3]
            new_product.description = ' '.join(full_info[3:])
            categories = []
            for cat in full_info[2].split(' '):
                categories.append({'id': int(cat) })
            new_product.categories = categories
        os.chdir('..')


class Product:
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


class Products_Validator(Application):
    VALID = []
    INVALID_THUMBNAILS = []
    INVALID_INFO = []

    def __init__(self):
        self.check_folders()
        self.report_valid()
        self.report_invalid_thumbnails()
        self.report_invalid_info()

    def check_folders(self) -> None:
        os.chdir('products')
        products_folder = os.getcwd()
        for product_name in os.listdir(products_folder):
            if self.check_thumbnails_exists(product_name) and self.check_product_info_exists(product_name):
                Products_Validator.VALID.append(product_name)
            elif self.check_thumbnails_exists(product_name) == False:
                Products_Validator.INVALID_THUMBNAILS.append(product_name)
            elif self.check_product_info_exists(product_name) == False:
                Products_Validator.INVALID_INFO.append(product_name)
        os.chdir('..')

    @staticmethod
    def report_valid():
        print('Prawidłowe foldery:')
        for name in Products_Validator.VALID:
            print(name)
        print('----------------------')

    @staticmethod
    def report_invalid_thumbnails():
        print('Foldery bez miniaturek:')
        for name in Products_Validator.INVALID_THUMBNAILS:
            print(name)
        print('----------------------')

    @staticmethod
    def report_invalid_info():
        print('Foldery bez pliku info.txt:')
        for name in Products_Validator.INVALID_INFO:
            print(name)
        print('----------------------')




if __name__ == '__main__':
    app = Application()
    app.main()



