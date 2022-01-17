
from api.models import User
from factory import django, Faker


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    password = "Password123"
    location = "UK"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        # The default would use ``manager.create(*args, **kwargs)``
        return User.objects.create_user(*args, **kwargs)
