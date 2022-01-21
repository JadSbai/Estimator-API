"""The database seeder."""
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from faker import Faker
import random
from api.models import User
from django.utils import timezone


class Command(BaseCommand):
    RANDOM_USERS_LIST = None
    PASSWORD = "Password123"
    USER_SIZE = 50
    PRODUCTS_LIST = []

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        user_count = 0

        try:
            Command.JEAN = self._create_specific_user('Jean', 'Michel', 'jean.michel@example.org')
            Command.SPECIFIC_USERS_LIST = [Command.JEAN]
            user_count += 1
        except IntegrityError:
            print("You have already created the specific users")

        while user_count < Command.USER_SIZE:
            try:
                user = self._create_random_user()
                Command.RANDOM_USERS_LIST.append(user)
                user_count += 1
            except IntegrityError:
                print("This user already exists")
                continue

    def _create_specific_user(self, first_name, last_name, email):
        """Creating specific user"""
        user = self._create_user_instance(first_name, last_name, email)
        return user

    def _create_random_user(self):
        """Creating random user."""

        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self._email(first_name, last_name)
        user = self._create_user_instance(first_name, last_name, email)
        return user

    def _create_user_instance(self, first_name, last_name, email):
        """Creating a user instance according to given parameters"""
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            location="UK",
            password=Command.PASSWORD
        )
        return user

    def _email(self, first_name, last_name):
        email = '' + first_name.lower() + '.' + last_name.lower() + '@example.org'
        return email
