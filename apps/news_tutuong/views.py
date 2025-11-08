from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import NewsMonthTuTuong, DanhSachQuanNhan, KetQuaPhanLoai
from .serializers import (
    NewsMonthTuTuongSerializer, 
    DanhSachQuanNhanSerializer, 
    KetQuaPhanLoaiSerializer
)

@extend_schema_view(
    list=extend_schema(description="Lấy danh sách tất cả các tháng tư tưởng"),
    create=extend_schema(description="Tạo mới một tháng tư tưởng"),
    retrieve=extend_schema(description="Lấy chi tiết một tháng tư tưởng"),
    update=extend_schema(description="Cập nhật thông tin tháng tư tưởng"),
    destroy=extend_schema(description="Xóa tháng tư tưởng"),
)
class NewsMonthTuTuongViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho quản lý các tháng tư tưởng.
    
    list:
        Lấy danh sách tất cả các tháng tư tưởng
    create:
        Tạo mới một tháng tư tưởng
    retrieve:
        Lấy chi tiết một tháng tư tưởng
    update:
        Cập nhật thông tin tháng tư tưởng
    destroy:
        Xóa tháng tư tưởng
    """
    queryset = NewsMonthTuTuong.objects.all()
    serializer_class = NewsMonthTuTuongSerializer

    @extend_schema(description="Lấy danh sách quân nhân theo tháng tư tưởng")
    @action(detail=True, methods=['get'])
    def danh_sach_quan_nhan(self, request, pk=None):
        """
        Lấy danh sách quân nhân theo tháng tư tưởng
        """
        news_month = self.get_object()
        danh_sach = DanhSachQuanNhan.objects.filter(news_month=news_month)
        serializer = DanhSachQuanNhanSerializer(danh_sach, many=True)
        return Response(serializer.data)

    @extend_schema(description="Lấy kết quả phân loại theo tháng tư tưởng")
    @action(detail=True, methods=['get'])
    def ket_qua_phan_loai(self, request, pk=None):
        """
        Lấy kết quả phân loại theo tháng tư tưởng
        """
        news_month = self.get_object()
        ket_qua = KetQuaPhanLoai.objects.filter(news_month=news_month)
        serializer = KetQuaPhanLoaiSerializer(ket_qua, many=True)
        return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(description="Lấy danh sách tất cả quân nhân"),
    create=extend_schema(description="Tạo mới một quân nhân"),
    retrieve=extend_schema(description="Lấy chi tiết một quân nhân"),
    update=extend_schema(description="Cập nhật thông tin quân nhân"),
    destroy=extend_schema(description="Xóa quân nhân"),
)
class DanhSachQuanNhanViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho quản lý danh sách quân nhân.
    
    list:
        Lấy danh sách tất cả quân nhân
    create:
        Tạo mới một quân nhân
    retrieve:
        Lấy chi tiết một quân nhân
    update:
        Cập nhật thông tin quân nhân
    destroy:
        Xóa quân nhân
    """
    queryset = DanhSachQuanNhan.objects.all()
    serializer_class = DanhSachQuanNhanSerializer

    def get_queryset(self):
        queryset = DanhSachQuanNhan.objects.all()
        news_month_id = self.request.query_params.get('news_month', None)
        if news_month_id is not None:
            queryset = queryset.filter(news_month_id=news_month_id)
        return queryset

@extend_schema_view(
    list=extend_schema(description="Lấy danh sách tất cả kết quả phân loại"),
    create=extend_schema(description="Tạo mới một kết quả phân loại"),
    retrieve=extend_schema(description="Lấy chi tiết một kết quả phân loại"),
    update=extend_schema(description="Cập nhật thông tin kết quả phân loại"),
    destroy=extend_schema(description="Xóa kết quả phân loại"),
)
class KetQuaPhanLoaiViewSet(viewsets.ModelViewSet):
    """
    ViewSet cho quản lý kết quả phân loại.
    
    list:
        Lấy danh sách tất cả kết quả phân loại
    create:
        Tạo mới một kết quả phân loại
    retrieve:
        Lấy chi tiết một kết quả phân loại
    update:
        Cập nhật thông tin kết quả phân loại
    destroy:
        Xóa kết quả phân loại
    """
    queryset = KetQuaPhanLoai.objects.all()
    serializer_class = KetQuaPhanLoaiSerializer

    def get_queryset(self):
        queryset = KetQuaPhanLoai.objects.all()
        news_month_id = self.request.query_params.get('news_month', None)
        if news_month_id is not None:
            queryset = queryset.filter(news_month_id=news_month_id)
        return queryset 