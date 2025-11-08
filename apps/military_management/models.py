from django.db import models
import uuid

def generate_company_id():
    return f"company-{uuid.uuid4()}"

def generate_soldier_id():
    return f"soldier-{uuid.uuid4()}"

class Company(models.Model):
    """Model cho Đại đội"""
    id = models.CharField(primary_key=True, max_length=50, default=generate_company_id, editable=False)
    name = models.CharField(max_length=100, verbose_name="Tên đại đội")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Đại đội"
        verbose_name_plural = "Đại đội"
        ordering = ['name']

    def __str__(self):
        return self.name

class Soldier(models.Model):
    """Model cho Chiến sỹ"""
    id = models.CharField(primary_key=True, max_length=50, default=generate_soldier_id, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='soldiers', verbose_name="Đại đội")
    
    # Thông tin cơ bản
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    birth_date = models.DateField(verbose_name="Ngày sinh")
    soldier_rank = models.CharField(max_length=50, verbose_name="CB")  # Cấp bậc
    soldier_position = models.CharField(max_length=50, verbose_name="CV")  # Chức vụ
    place_work = models.CharField(max_length=100, verbose_name="ĐV") # Đơn vị làm việc
    join_union_party_date = models.DateField(null=True, blank=True, verbose_name="Ngày vào Đoàn/ Đảng")
    # Thông tin cá nhân
    ethnicity = models.CharField(max_length=50, verbose_name="Dân tộc")
    education = models.CharField(max_length=100, verbose_name="Văn hóa")
    religion = models.CharField(max_length=50, blank=True, verbose_name="Tôn giáo")
    hometown = models.CharField(max_length=200, verbose_name="Quê quán")
    father_name = models.CharField(max_length=100, verbose_name="Họ tên bố")
    mother_name = models.CharField(max_length=100, verbose_name="Họ tên mẹ")
    phone_number = models.CharField(max_length=100, verbose_name="Số điện thoại")
    
    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chiến sỹ"
        verbose_name_plural = "Chiến sỹ"
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} - {self.company.name}"