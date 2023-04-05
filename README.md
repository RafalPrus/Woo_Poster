# Woo_Poster
This Python application allows you to automate the process of adding new products to your online store based on WordPress and WooCommerce. With this tool, you can quickly and easily upload product information, images, and pricing data, saving you time and effort.

[![Python Version](https://img.shields.io/badge/python-3.10.6-blue.svg)](https://www.python.org/downloads/release/python-3.10.6/)


## Getting Started
To use this tool, you will need to have Python 3.6 or higher installed on your system. Once you have those installed, clone this repository by running the following command in your terminal
```bash
git clone https://github.com/RafalPrus/Woo_Poster.git
```
Then, install all necessary dependencies with:
```bash
pip install -r requirements.txt
```

## Usage
To use this application, you need to and put catalogs into 'products' folder with the products you want to add to your website according to this specification:

The product catalog must contain:
1. A 'small' folder containing thumbnail images, which will be uploaded to the website.
2. An 'info.txt' file containing all the necessary information about the product (product title, description, price, category numbers) according to this schema:
```bash
MAIN CATEGORY
Product ID
Category numbers to which the product should be added, taken from your website
Product title

Product description
```
for example:
```bash
CARS
239203
33 711
Alfa Romeo Giulia

Beautiful and fast car from the well-known Italian brand. 
Available exclusively by order at our dealerships!
```
3. 


