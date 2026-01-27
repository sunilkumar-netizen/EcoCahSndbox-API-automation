"""
Data Generator Module
Provides utilities for generating test data dynamically.
Uses Faker library for realistic test data generation.
"""

from faker import Faker
import random
import string
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List


class DataGenerator:
    """
    Test data generator using Faker library.
    Generates realistic test data for API automation.
    """
    
    def __init__(self, locale: str = 'en_US'):
        """
        Initialize data generator.
        
        Args:
            locale: Faker locale (default: en_US)
        """
        self.faker = Faker(locale)
        Faker.seed(0)  # For reproducible tests
    
    def generate_user_data(self) -> Dict[str, Any]:
        """
        Generate random user data.
        
        Returns:
            Dictionary with user details
        """
        return {
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'email': self.faker.email(),
            'phone': self.faker.phone_number(),
            'username': self.faker.user_name(),
            'password': self.generate_password(),
            'date_of_birth': self.faker.date_of_birth(minimum_age=18, maximum_age=65).isoformat(),
            'address': {
                'street': self.faker.street_address(),
                'city': self.faker.city(),
                'state': self.faker.state(),
                'zip_code': self.faker.zipcode(),
                'country': self.faker.country_code()
            }
        }
    
    def generate_payment_data(self, amount_range: tuple = (10, 1000)) -> Dict[str, Any]:
        """
        Generate random payment data.
        
        Args:
            amount_range: Tuple of (min, max) amount
            
        Returns:
            Dictionary with payment details
        """
        return {
            'transaction_id': str(uuid.uuid4()),
            'amount': round(random.uniform(*amount_range), 2),
            'currency': random.choice(['USD', 'EUR', 'GBP', 'ZWL']),
            'payment_method': random.choice(['card', 'mobile_money', 'bank_transfer']),
            'description': self.faker.sentence(),
            'timestamp': datetime.now().isoformat(),
            'merchant_id': self.generate_merchant_id(),
            'customer': {
                'name': self.faker.name(),
                'email': self.faker.email(),
                'phone': self.generate_phone_number()
            }
        }
    
    def generate_phone_number(self, country_code: str = '+263') -> str:
        """
        Generate random phone number.
        
        Args:
            country_code: Country code prefix
            
        Returns:
            Phone number string
        """
        number = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        return f"{country_code}{number}"
    
    def generate_merchant_id(self, prefix: str = 'MCH') -> str:
        """
        Generate merchant ID.
        
        Args:
            prefix: Merchant ID prefix
            
        Returns:
            Merchant ID string
        """
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return f"{prefix}{random_part}"
    
    def generate_password(self, length: int = 12) -> str:
        """
        Generate secure random password.
        
        Args:
            length: Password length
            
        Returns:
            Password string
        """
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    
    def generate_email(self, domain: str = None) -> str:
        """
        Generate email address.
        
        Args:
            domain: Email domain (optional)
            
        Returns:
            Email address
        """
        if domain:
            username = self.faker.user_name()
            return f"{username}@{domain}"
        return self.faker.email()
    
    def generate_uuid(self) -> str:
        """
        Generate UUID.
        
        Returns:
            UUID string
        """
        return str(uuid.uuid4())
    
    def generate_timestamp(self, days_offset: int = 0) -> str:
        """
        Generate ISO timestamp.
        
        Args:
            days_offset: Days to add/subtract from current date
            
        Returns:
            ISO formatted timestamp
        """
        date = datetime.now() + timedelta(days=days_offset)
        return date.isoformat()
    
    def generate_random_string(self, length: int = 10, 
                               chars: str = string.ascii_letters) -> str:
        """
        Generate random string.
        
        Args:
            length: String length
            chars: Character set to use
            
        Returns:
            Random string
        """
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_random_number(self, min_val: int = 1, max_val: int = 100) -> int:
        """
        Generate random number.
        
        Args:
            min_val: Minimum value
            max_val: Maximum value
            
        Returns:
            Random integer
        """
        return random.randint(min_val, max_val)
    
    def generate_credit_card(self) -> Dict[str, str]:
        """
        Generate credit card data.
        
        Returns:
            Dictionary with card details
        """
        return {
            'number': self.faker.credit_card_number(),
            'provider': self.faker.credit_card_provider(),
            'cvv': self.faker.credit_card_security_code(),
            'expiry_date': self.faker.credit_card_expire(),
            'holder_name': self.faker.name()
        }
    
    def generate_company_data(self) -> Dict[str, Any]:
        """
        Generate company data.
        
        Returns:
            Dictionary with company details
        """
        return {
            'name': self.faker.company(),
            'email': self.faker.company_email(),
            'phone': self.faker.phone_number(),
            'website': self.faker.url(),
            'registration_number': self.generate_random_string(10, string.digits),
            'address': {
                'street': self.faker.street_address(),
                'city': self.faker.city(),
                'country': self.faker.country()
            }
        }
    
    def pick_random_from_list(self, items: List[Any]) -> Any:
        """
        Pick random item from list.
        
        Args:
            items: List of items
            
        Returns:
            Random item
        """
        return random.choice(items)
