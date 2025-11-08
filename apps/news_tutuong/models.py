from django.db import models

class NewsMonthTuTuong(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class DanhSachQuanNhan(models.Model):
    news_month = models.ForeignKey(NewsMonthTuTuong, on_delete=models.CASCADE, related_name='danh_sach_quan_nhan')
    ho_va_ten = models.CharField(max_length=255)
    cb = models.CharField(max_length=100, blank=True, null=True)  # Cán bộ
    cv = models.CharField(max_length=100, blank=True, null=True)  # Chức vụ
    dv = models.CharField(max_length=100, blank=True, null=True)  # Đơn vị
    ly_do = models.TextField(blank=True, null=True)
    ghi_chu = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ho_va_ten

class KetQuaPhanLoai(models.Model):
    news_month = models.ForeignKey(NewsMonthTuTuong, on_delete=models.CASCADE, related_name='ket_qua_phan_loai')
    doi_tuong = models.CharField(max_length=255)
    du_phan_loai_tong_so = models.CharField(max_length=100)  # Dự phân loại/tổng số
    tot = models.IntegerField(default=0)
    kha = models.IntegerField(default=0)
    trung_binh = models.IntegerField(default=0)
    yeu = models.IntegerField(default=0)
    guong_tot_viec_tot = models.IntegerField(default=0)
    khen_thuong = models.IntegerField(default=0)
    ky_luat = models.IntegerField(default=0)

    def __str__(self):
        return self.doi_tuong 