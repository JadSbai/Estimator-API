from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    """Custom manager for creation of users and superusers"""

    def create_user(self, email, first_name, last_name, location, password=None,
                    is_admin=False, is_staff=False, is_active=True):
        """Create a user according to User model"""
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not location:
            raise ValueError("User must have a location")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.location = location
        user.set_password(password)  # change password to hash
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create a super user with email and password only"""
        if not email:
            raise ValueError("Superuser must have an email")
        if not password:
            raise ValueError("Superuser must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """User model"""
    username = None  # Don't use the username field inherited from the AbstractUser Model
    first_name = models.CharField(max_length=50, blank=False, null=True)
    last_name = models.CharField(max_length=50, blank=False, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    location = models.CharField(max_length=520, blank=True, null=False)
    USERNAME_FIELD = 'email'  # A user is identified by their email
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        ordering = ['email']


class ProviderManager(models.Manager):
    """Custom manager for creation of providers"""

    def get_or_create_provider(self, name):
        """Create a provider according to Provider model or retrieve existing provider"""

        if not name:
            raise ValueError("Provider must have a name")

        if Provider.objects.filter(name=name):
            return Provider.objects.get(name=name)
        else:
            provider = self.model()
            provider.name = name
            provider.save(using=self._db)
            return provider


class Provider(models.Model):
    """Provider model"""
    name = models.CharField(max_length=50, default="Amazon", unique=True)
    objects = ProviderManager()

    class Meta:
        ordering = ['name']


class ProductManager(models.Manager):
    """Custom manager used for creation of products"""

    def get_or_create_product(self, description, provider):
        """Create a product according to Product model or retrieve existing product"""

        if not description:
            raise ValueError("Product must have a description")
        if not provider:
            raise ValueError("Product must have a provider")

        if Product.objects.filter(description=description, provider=provider):
            return Product.objects.get(description=description, provider=provider)
        else:
            product = self.model()
            product.description = description
            product.provider = Provider.objects.get_or_create_provider(provider)
            product.save(using=self._db)
            return product


class Product(models.Model):
    """Product model"""
    description = models.JSONField()
    provider = models.ForeignKey(Provider, on_delete=models.DO_NOTHING, related_name="known_products")
    objects = ProductManager()

    class Meta:
        unique_together = ["description", "provider"]
        ordering = ['id']


class ResultManager(models.Manager):
    """Custom manager used for creation of results"""

    def get_or_create_result(self, suggested_product):
        """Create a result according to Result model or retrieve existing result"""

        if not suggested_product:
            raise ValueError("Result must have a suggested product")

        if Result.objects.filter(suggested_product=suggested_product):
            return Result.objects.get(suggested_product=suggested_product)
        else:
            result = self.model()
            result.suggested_product = suggested_product
            result.save(using=self._db)
            return result


class Result(models.Model):
    """Result model"""
    suggested_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="suggestions")
    objects = ResultManager()

    class Meta:
        ordering = ['id']


class SearchManager(models.Manager):
    """Custom manager used for creation of searches"""

    def create_search(self, user, date, searched_product, is_buy, suggested_product_description, provider):
        """Create a search object"""

        if not user:
            raise ValueError("Search must have a user")
        if not date:
            raise ValueError("Search must have a date")
        if not searched_product:
            raise ValueError("Search must have a searched product")
        if not is_buy:
            raise ValueError("Search must have a is_buy")

        search = self.model()
        search.user = User.objects.get(email=user)
        search.date = date
        search.searched_product = searched_product
        search.is_buy = is_buy
        if suggested_product_description and provider:
            search.result = Result.objects.get_or_create_result(
                Product.objects.get_or_create_product(suggested_product_description,
                                                      Provider.objects.get_or_create_provider(provider)))
        search.save(using=self._db)
        return search


class Search(models.Model):
    """Search model"""

    user = models.ForeignKey(User, related_name="my_searches", on_delete=models.CASCADE)
    date = models.DateTimeField()
    searched_product = models.CharField(max_length=1000)
    is_buy = models.BooleanField(default=True)
    result = models.ForeignKey(Result, on_delete=models.DO_NOTHING, related_name="searches", null=True)
    objects = SearchManager()

    class Meta:
        unique_together = ["user", "date"]
        ordering = ['user', '-date']
