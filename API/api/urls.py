from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView # type: ignore
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView, TokenBlacklistView # type: ignore

app_name = "api"

router = DefaultRouter()
urlpatterns = [
   
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name="token_verify"),
    path('token/blacklist/', TokenBlacklistView.as_view(), name="token_blacklist"),  
    #path('personal/', include('api.personal.urls')),  
    path('', include(router.urls)),
    path('user/', include('api.user.urls')),  

]

