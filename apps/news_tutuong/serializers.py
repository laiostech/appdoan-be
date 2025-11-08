from rest_framework import serializers
from .models import NewsMonthTuTuong, DanhSachQuanNhan, KetQuaPhanLoai

class NewsMonthTuTuongSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsMonthTuTuong
        fields = ['id', 'name']

class DanhSachQuanNhanSerializer(serializers.ModelSerializer):
    news_month_name = serializers.CharField(source='news_month.name', read_only=True)
    
    class Meta:
        model = DanhSachQuanNhan
        fields = [
            'id', 'news_month', 'news_month_name', 'ho_va_ten', 
            'cb', 'cv', 'dv', 'ly_do', 'ghi_chu'
        ]

class KetQuaPhanLoaiSerializer(serializers.ModelSerializer):
    news_month_name = serializers.CharField(source='news_month.name', read_only=True)
    
    class Meta:
        model = KetQuaPhanLoai
        fields = [
            'id', 'news_month', 'news_month_name', 'doi_tuong',
            'du_phan_loai_tong_so', 'tot', 'kha', 'trung_binh', 'yeu',
            'guong_tot_viec_tot', 'khen_thuong', 'ky_luat'
        ] 