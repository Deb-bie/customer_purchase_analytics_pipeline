from pathlib import Path
import random
from faker import Faker # type: ignore
import pandas as pd # type: ignore
from datetime import datetime


class CustomerDataGenerator:

    '''
    Generate synthetic customer data using Faker
    '''


    def __init__(self, 
                 num_customers: int = 1000,
                 start_date: str = '2024-01-01', 
                 end_date: str = '2025-05-01',
                 output_path="data/raw/customers.csv"
                ):
        self.num_of_customers = num_customers
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')

        self.fake = Faker()
        Faker.seed(42)
        random.seed(42)


    def generate_customers(self):
        print(f"Generating {self.num_of_customers} customers...")

        customers = []

        for i in range(1, self.num_of_customers+1):
            gender = self.fake.random_element(['Male', 'Female'])
            first_name = (self.fake.first_name_male() if gender == 'Male' else self.fake.first_name_female())
            birth_date = self.fake.date_of_birth(minimum_age=18, maximum_age=70)
            
            customers.append({
                "customer_id": i,
                "first_name": first_name,
                "last_name": self.fake.last_name(),
                "email": self.fake.email(),
                'phone': self.fake.phone_number(),
                "birth_date": birth_date,
                "age": (datetime.now().date() - birth_date).days // 365,
                "gender": gender,
                "signup_date": self.fake.date_between(start_date=self.start_date, end_date=self.end_date),
                'city': self.fake.city(),
                'state': self.fake.state(),
                'country': 'United States',
                "loyalty_tier": random.choice(["Bronze","Silver","Gold","Platinum"])
            })
        
        df = pd.DataFrame(customers)
        df.to_csv(self.output_path, index=False)
        



