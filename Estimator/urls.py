"""Estimator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from api import views
from api.views import SearchViewSet, ResultViewSet, ProductViewSet, UserViewSet, ProviderViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin

search_list = SearchViewSet.as_view({
    'get': 'list',
    'post': 'create'

})

get_search = SearchViewSet.as_view({
    'get': 'retrieve'
})

get_result = ResultViewSet.as_view({
    'get': 'retrieve'
})

result_list = ResultViewSet.as_view({
    'get': 'list'
})

get_product = ProductViewSet.as_view({
    'get': 'retrieve'
})

product_list = ProductViewSet.as_view({
    'get': 'list'
})

get_provider = ProviderViewSet.as_view({
    'get': 'retrieve'
})

provider_list = ProviderViewSet.as_view({
    'get': 'list'
})

get_user = UserViewSet.as_view({
    'get': 'retrieve',
})

user_list = UserViewSet.as_view({
    'get': 'list',
})

sign_up = UserViewSet.as_view({
    'post': 'create',
})

login = TokenObtainPairView.as_view()
login_refresh = TokenRefreshView.as_view()

change_password = UserViewSet.as_view({
    'patch': 'set_password',
})


urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('admin/', admin.site.urls),
    path('sign-up/', sign_up, name='sign_up'),
    path('login/', login, name='login'),
    path('login/refresh/', login_refresh, name='login_refresh'),
    path('searches/', search_list, name='search_list'),
    path('results/', result_list, name='result_list'),
    path('products/', product_list, name='product_list'),
    path('providers/', provider_list, name='provider_list'),
    path('users/', user_list, name='user_list'),
    path('searches/<int:pk>', get_search, name='get_search'),
    path('results/<int:pk>', get_result, name='get_result'),
    path('products/<int:pk>', get_product, name='get_product'),
    path('providers/<int:pk>', get_provider, name='get_provider'),
    path('users/<int:pk>', get_user, name='get_user'),
    path('users/<int:pk>/password/', change_password, name='change_password'),
])
