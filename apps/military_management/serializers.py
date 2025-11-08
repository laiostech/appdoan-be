from rest_framework import serializers
from .models import Company, Soldier

class CompanySerializer(serializers.ModelSerializer):
    soldiers_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'soldiers_count', 'created_at', 'updated_at']
        
    def get_soldiers_count(self, obj):
        return obj.soldiers.count()

class SoldierSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    # Thêm fields tương thích ngược cho frontend
    rank = serializers.CharField(source='soldier_rank', read_only=True)
    position = serializers.CharField(source='soldier_position', read_only=True)
    
    class Meta:
        model = Soldier
        fields = [
            'id', 'company', 'company_name', 'full_name', 'birth_date', 
            'soldier_rank', 'soldier_position', 'place_work', 'rank', 'position',
            'join_union_party_date', 'ethnicity', 'education', 'religion', 
            'hometown', 'father_name', 'mother_name', 'phone_number',
            'created_at', 'updated_at'
        ]

class SoldierCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer cho việc tạo và cập nhật chiến sỹ"""
    
    class Meta:
        model = Soldier
        fields = [
            'company', 'full_name', 'birth_date', 'soldier_rank', 'soldier_position',
            'place_work', 'join_union_party_date', 'ethnicity', 'education', 
            'religion', 'hometown', 'father_name', 'mother_name', 'phone_number'
        ]

class CompanyDetailSerializer(serializers.ModelSerializer):
    """Serializer chi tiết cho đại đội bao gồm danh sách chiến sỹ"""
    soldiers = SoldierSerializer(many=True, read_only=True)
    soldiers_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'soldiers', 'soldiers_count', 'created_at', 'updated_at']
        
    def get_soldiers_count(self, obj):
        return obj.soldiers.count() 