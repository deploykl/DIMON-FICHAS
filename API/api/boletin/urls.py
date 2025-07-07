from django.urls import path
from rest_framework.routers import DefaultRouter
from api.boletin.views import *

router = DefaultRouter()

router.register(r'boletin', BoletinViewSet)


urlpatterns = router.urls
