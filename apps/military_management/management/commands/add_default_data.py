from django.core.management.base import BaseCommand
from apps.military_management.models import Company

class Command(BaseCommand):
    help = 'Thêm dữ liệu mặc định cho military management'

    def handle(self, *args, **options):
        # Tạo Đại đội 12
        company, created = Company.objects.get_or_create(
            id='1',
            defaults={
                'name': 'Đại đội 12',
                'description': 'thuộc tiểu đoàn BB3'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Đã tạo: {company.name} - {company.description}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Đã tồn tại: {company.name}')
            )
        
        # Hiển thị thông tin
        self.stdout.write(f'ID: {company.id}')
        self.stdout.write(f'Tên: {company.name}')
        self.stdout.write(f'Mô tả: {company.description}')
        self.stdout.write(f'Tạo lúc: {company.created_at}')
        self.stdout.write(f'Cập nhật: {company.updated_at}') 