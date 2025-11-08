from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsMonthTuTuongViewSet, DanhSachQuanNhanViewSet, KetQuaPhanLoaiViewSet

router = DefaultRouter()
router.register(r'news-months', NewsMonthTuTuongViewSet)
router.register(r'danh-sach-quan-nhan', DanhSachQuanNhanViewSet)
router.register(r'ket-qua-phan-loai', KetQuaPhanLoaiViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 