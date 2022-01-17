import json
from api.models import User, Product, Result, Search, Provider
from api.serializers import UserSerializer, ProductSerializer, SearchSerializer, ResultSerializer, ProviderSerializer,\
    SignUpSerializer, PasswordSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
import requests
from rest_framework.permissions import IsAuthenticated
from api.helpers import get_best_product
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action


@api_view(['GET'])
def api_root(request, format=None):
    """Root of the API"""
    return Response({
        'searches': reverse('make_search', request=request, format=format),
    })


class SearchViewSet(viewsets.ModelViewSet):
    """API endpoint that allows to make and get searches."""
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['user']

    def create(self, request, *args, **kwargs):
        product = request.query_params['data']
        date = request.query_params['date']

        if product == "":
            return Response({'custom_message': "You have not entered a valid a search"},
                            status=status.HTTP_400_BAD_REQUEST)

        url = f"https://amazon-data-scrapper3.p.rapidapi.com/search/{product}"

        querystring = {"api_key": "10518d369acaf28f525da1e0e8039add"}

        headers = {
            'x-rapidapi-host': "amazon-data-scrapper3.p.rapidapi.com",
            'x-rapidapi-key': "301d4e1a20mshcaa6572657b534fp107484jsnb6b5217354cb"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        try:
            best_product = get_best_product(response.text)
        except json.decoder.JSONDecodeError:
            return Response({'custom_message': "The Amazon API failed"}, status=status.HTTP_200_OK)
        else:
            clean_best_product = json.dumps(best_product)

            new_result = None
            if best_product:
                new_result = {'suggested_product': {'description': clean_best_product, 'provider': {'name': "Amazon"}}}

            data = {'searched_product': product, 'date': date, 'is_buy': True, 'user': {'email': request.user.email},
                    'result': new_result}

            serializer = SearchSerializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ResultViewSet(viewsets.ModelViewSet):
    """API endpoint that allows to get results."""
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    """API endpoint that allows to get products."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProviderViewSet(viewsets.ModelViewSet):
    """API endpoint that allows to get providers."""
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows to sign up users, change their password and retrieve them."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        new_user = User.objects.get(email=request.data['email'])
        refresh = RefreshToken.for_user(new_user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def set_password(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = PasswordSerializer(user, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'password successfully changed'}, status=status.HTTP_200_OK)
