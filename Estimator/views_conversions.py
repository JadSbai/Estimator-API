from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import SearchViewSet, ResultViewSet, ProductViewSet, UserViewSet, ProviderViewSet

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