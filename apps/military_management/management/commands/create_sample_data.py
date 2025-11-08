from django.core.management.base import BaseCommand
from apps.military_management.models import Company, Soldier
from datetime import date

class Command(BaseCommand):
    help = 'Tạo dữ liệu mẫu cho quản lý quân sự'

    def handle(self, *args, **options):
        # Đảm bảo company ID='1' tồn tại
        try:
            company = Company.objects.get(id='1')
            self.stdout.write(f'✅ Sử dụng: {company.name}')
        except Company.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Chưa có Đại đội 12. Hãy chạy: python manage.py add_default_data'))
            return

        # Danh sách chiến sỹ theo SQL
        soldiers_data = [
            {
                'id': '1',
                'company': company,
                'full_name': 'Nguyễn Đình Quang',
                'birth_date': date(2005, 7, 4),
                'soldier_rank': 'H2',
                'soldier_position': 'kđt',
                'place_work': 'Kđ1',
                'join_union_party_date': None,
                'ethnicity': 'Kinh',
                'education': '9/12',
                'religion': 'Không',
                'hometown': 'Quảng Phú, Thanh Hóa',
                'father_name': 'Nguyễn Đình Cảnh',
                'mother_name': 'Lò Thị Chung',
                'phone_number': '0372442421'
            },
            {
                'id': '2',
                'company': company,
                'full_name': 'Lê Văn Vũ',
                'birth_date': date(2003, 11, 30),
                'soldier_rank': 'B2',
                'soldier_position': 'cs',
                'place_work': 'Kđ1',
                'join_union_party_date': None,
                'ethnicity': 'Kinh',
                'education': 'CĐ',
                'religion': 'Không',
                'hometown': 'Hải Bình, Quãng Trị',
                'father_name': 'Lê Văn Bảy',
                'mother_name': 'Lê Thị Phương Nhị',
                'phone_number': '0966761946'
            },
            {
                'id': '3',
                'company': company,
                'full_name': 'Phan Thế Duẩn',
                'birth_date': date(2006, 8, 10),
                'soldier_rank': 'B2',
                'soldier_position': 'cs',
                'place_work': 'Kđ1',
                'join_union_party_date': None,
                'ethnicity': 'Kinh',
                'education': '9/12',
                'religion': 'Không',
                'hometown': 'Sầm Sơn, Thanh Hóa',
                'father_name': 'Phan Thế Thế',
                'mother_name': 'Nguyễn Thị Hà',
                'phone_number': '0339187430'
            }
        ]

        # Tạo các chiến sỹ
        created_count = 0
        for data in soldiers_data:
            soldier, created = Soldier.objects.get_or_create(
                id=data['id'],
                defaults=data
            )
            
            if created:
                self.stdout.write(f'✅ Đã tạo: {soldier.full_name} (ID: {soldier.id})')
                created_count += 1
            else:
                self.stdout.write(f'⚠️ Đã tồn tại: {soldier.full_name} (ID: {soldier.id})')

        # Tổng kết
        self.stdout.write(self.style.SUCCESS(f'\n🎯 Hoàn thành! Đã tạo {created_count} chiến sỹ mới.'))
        self.stdout.write(f'📊 Tổng số đại đội: {Company.objects.count()}')
        self.stdout.write(f'📊 Tổng số chiến sỹ: {Soldier.objects.count()}') 