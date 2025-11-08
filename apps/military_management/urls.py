from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, SoldierViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'soldiers', SoldierViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 