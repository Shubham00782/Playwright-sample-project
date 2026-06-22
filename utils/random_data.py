from faker import Faker
import random
import string

# Initialize Faker
fake = Faker()

class RandomDataGenerator:
    """
    Utility class to generate random data using the Faker library.
    This provides static methods to generate various types of mock data 
    useful for automated testing (users, addresses, products, etc.).
    """

    @staticmethod
    def generate_user_data():
        """
        Generates comprehensive random user registration/profile data.
        
        :return: Dictionary containing user details.
        """
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "telephone": fake.phone_number(),
            "password": fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
            "company": fake.company()
        }

    @staticmethod
    def generate_address_data():
        """
        Generates random address data.
        
        :return: Dictionary containing address details.
        """
        return {
            "address_1": fake.street_address(),
            "address_2": fake.secondary_address(),
            "city": fake.city(),
            "postcode": fake.postcode(),
            "country": fake.country(),
            "state": fake.state()
        }

    @staticmethod
    def generate_random_email():
        """
        Generates a unique random email address.
        
        :return: Random email string.
        """
        return fake.unique.email()

    @staticmethod
    def generate_random_password(length=12):
        """
        Generates a strong random password.
        
        :param length: Length of the password. Default is 12.
        :return: Random password string.
        """
        return fake.password(length=length, special_chars=True, digits=True, upper_case=True, lower_case=True)

    @staticmethod
    def generate_random_string(length=10):
        """
        Generates a random alphanumeric string.
        
        :param length: Length of the string. Default is 10.
        :return: Random alphanumeric string.
        """
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))

    @staticmethod
    def generate_product_data():
        """
        Generates random product data for testing e-commerce functions.
        
        :return: Dictionary containing product details.
        """
        return {
            "name": fake.catch_phrase(),
            "description": fake.text(max_nb_chars=200),
            "price": round(random.uniform(10.0, 500.0), 2),
            "quantity": random.randint(1, 100)
        }
