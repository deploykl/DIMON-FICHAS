from django.urls import path
from rest_framework.routers import DefaultRouter
from api.enlaces.views import *

router = DefaultRouter()

router.register(r'urls', EnlaceViewSet)


urlpatterns = router.urls
