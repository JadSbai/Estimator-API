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
from django.urls import path
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
from Estimator.views_conversions import sign_up, login, login_refresh, search_list, user_list, result_list,\
    product_list, provider_list, get_result, get_product, get_provider, get_user, get_search, change_password


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
