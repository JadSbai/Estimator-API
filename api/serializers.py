from api.models import User, Product, Provider, Result, Search
from django.core.validators import RegexValidator
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'first_name', 'email', 'last_name', 'location']
        extra_kwargs = {
            'url': {'view_name': 'get_user'},
            'email': {'validators': []},
        }


class SignUpSerializer(serializers.HyperlinkedModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['url', 'first_name', 'email', 'last_name', 'location', 'password', 'confirm_password']
        extra_kwargs = {
            'url': {'view_name': 'get_user'},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'location': {'required': True},
            'password': {'validators': [RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                message='Password must contain an uppercase character, a lowercase '
                        'character and a number.')], 'required': True},
            'confirm_password': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        if attrs['first_name'] == "":
            raise serializers.ValidationError({"first name": "Please enter a first name"})

        if attrs['last_name'] == "":
            raise serializers.ValidationError({"last name": "Please enter a last name"})

        if attrs['location'] == "":
            raise serializers.ValidationError({"location": "Please enter a location"})

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(email=validated_data['email'], password=validated_data['password'],
                                        first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                        location=validated_data['location'])


class PasswordSerializer(serializers.HyperlinkedModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    current_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['url', 'new_password', 'confirm_password', 'current_password']
        extra_kwargs = {
            'url': {'view_name': 'get_user'},
            'new_password': {'validators': [RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
                message='Password must contain an uppercase character, a lowercase '
                        'character and a number.')], 'required': True},
            'current_password': {'required': True},
            'confirm _password': {'required': True}
        }

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"new password": "Password fields didn't match."})

        if not check_password(attrs['current_password'], self.instance.password):
            raise serializers.ValidationError({"current password": "Password fields didn't match."})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = ['url', 'name']
        extra_kwargs = {
            'url': {'view_name': 'get_provider'},
            'name': {'validators': []},
        }


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    provider = ProviderSerializer()

    class Meta:
        model = Product
        fields = ['url', 'description', 'provider']
        extra_kwargs = {
            'url': {'view_name': 'get_product'},
        }

    def create(self, validated_data):
        return Product.objects.get_or_create_product(description=validated_data['description'],
                                                     provider=validated_data['provider']['name'])


class ResultSerializer(serializers.HyperlinkedModelSerializer):
    suggested_product = ProductSerializer()

    class Meta:
        model = Result
        fields = ['url', 'suggested_product']
        extra_kwargs = {
            'url': {'view_name': 'get_result'},
        }

    def create(self, validated_data):
        return Result.objects.get_or_create_result(description=validated_data['description'],
                                                   provider=validated_data['provider']['name'])


class SearchSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    result = ResultSerializer(required=False)

    class Meta:
        model = Search
        fields = ['url', 'searched_product', 'date', 'is_buy', 'result', 'user']
        extra_kwargs = {
            'url': {'view_name': 'get_search'},
        }

    def create(self, validated_data):
        return Search.objects.create_search(user=validated_data['user']['email'], date=validated_data['date'],
                                            searched_product=validated_data['searched_product'],
                                            is_buy=validated_data['is_buy'],
                                            suggested_product_description=
                                            validated_data['result']['suggested_product']['description'],
                                            provider_name=validated_data['result']['suggested_product']['provider']['name'])


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'user_id': self.user.id})
        # and everything else you want to send in the response
        return data
