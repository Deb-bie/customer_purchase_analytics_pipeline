from pathlib import Path
import random
from faker import Faker # type: ignore
import pandas as pd # type: ignore


class ProductDataGenerator:

    '''
    Generate synthetic product data using Faker
    '''


    def __init__(self, 
                 num_products: int = 500,
                 output_path="data/raw/products.csv"
                ):
        self.num_of_products = num_products
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        self.fake = Faker()
        Faker.seed(42)
        random.seed(42)


    categories = {
        'Electronics': {
            'subcategories': ['Smartphones', 'Laptops', 'Tablets', 'Accessories', 'Gaming'],
            'brands': ['Apple', 'Samsung', 'Sony', 'Dell', 'HP', 'Lenovo'],
            'price_range': (29, 3000)
        },
        'Clothing': {
            'subcategories': ['Men', 'Women', 'Kids', 'Shoes', 'Accessories'],
            'brands': ['Nike', 'Adidas', 'Zara', 'H&M', 'Levis', 'Gap'],
            'price_range': (15, 300)
        },
        'Home & Garden': {
            'subcategories': ['Furniture', 'Kitchen', 'Decor', 'Tools', 'Outdoor'],
            'brands': ['IKEA', 'Home Depot', 'Wayfair', 'Williams Sonoma'],
            'price_range': (20, 1200)
        },
        'Books': {
            'subcategories': ['Fiction', 'Non-Fiction', 'Educational', 'Comics'],
            'brands': ['Penguin', 'Random House', 'McGraw Hill', 'Marvel'],
            'price_range': (8, 80)
        },
        'Sports & Fitness': {
            'subcategories': ['Fitness', 'Outdoor', 'Team Sports', 'Water Sports'],
            'brands': ['Nike', 'Adidas', 'Under Armour', 'Wilson'],
            'price_range': (15, 800)
        }
    }


    def generate_products(self):
        print(f"Generating {self.num_of_products} products ...")

        products = []

        for i in range(1, self.num_of_products+1):
            category = random.choice(list(self.categories.keys()))
            category_info = self.categories[category]
            subcategory = random.choice(category_info['subcategories'])
            brand = random.choice(category_info['brands'])
            min_price, max_price = category_info['price_range']
            unit_price = round(self.fake.pyfloat(
                min_value=min_price, 
                max_value=max_price, 
                right_digits=2
            ), 2)
            cost_price = round(
                unit_price * self.fake.pyfloat(min_value=0.4, max_value=0.7), 
                2
            )
            sku = f"{brand[:3].upper()}-{category[:3].upper()}-{self.fake.bothify(text='###??').upper()}"

            products.append({
                "product_id": i,
                'sku': sku,
                "product_name": self.fake.word().title() + " " + self.fake.word().title(),
                "category": category,
                'subcategory': subcategory,
                'brand': brand,
                'unit_price': unit_price,
                'cost_price': cost_price,
                'weight_kg': round(self.fake.pyfloat(min_value=0.05, max_value=25.0), 3),
                'dimensions': f"{self.fake.random_int(5, 100)}x{self.fake.random_int(5, 100)}x{self.fake.random_int(5, 50)} cm",
                'color': self.fake.color_name(),
                'material': self.fake.random_element(['Plastic', 'Metal', 'Wood', 'Glass', 'Fabric', 'Leather']),
                'is_active': self.fake.boolean(chance_of_getting_true=95),
            })

        df = pd.DataFrame(products)
        df.to_csv(self.output_path, index=False)



