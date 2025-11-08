from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Company, Soldier
from .serializers import (
    CompanySerializer, 
    CompanyDetailSerializer,
    SoldierSerializer, 
    SoldierCreateUpdateSerializer
)

class CompanyViewSet(viewsets.ModelViewSet):
    """ViewSet cho quản lý Đại đội"""
    queryset = Company.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanySerializer
    
    def get_queryset(self):
        queryset = Company.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        return queryset

    @action(detail=True, methods=['get'])
    def soldiers(self, request, pk=None):
        """Lấy danh sách chiến sỹ của một đại đội"""
        company = self.get_object()
        soldiers = company.soldiers.all()
        
        # Tìm kiếm chiến sỹ
        search = request.query_params.get('search', None)
        if search:
            soldiers = soldiers.filter(
                Q(full_name__icontains=search) |
                Q(soldier_rank__icontains=search) |
                Q(soldier_position__icontains=search) |
                Q(place_work__icontains=search) |
                Q(phone_number__icontains=search)
            )
        
        serializer = SoldierSerializer(soldiers, many=True)
        return Response(serializer.data)

class SoldierViewSet(viewsets.ModelViewSet):
    """ViewSet cho quản lý Chiến sỹ"""
    queryset = Soldier.objects.select_related('company').all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SoldierCreateUpdateSerializer
        return SoldierSerializer
    
    def get_queryset(self):
        queryset = Soldier.objects.select_related('company').all()
        
        # Lọc theo đại đội
        company_id = self.request.query_params.get('company', None)
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        
        # Tìm kiếm
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) |
                Q(soldier_rank__icontains=search) |
                Q(soldier_position__icontains=search) |
                Q(place_work__icontains=search) |
                Q(phone_number__icontains=search) |
                Q(hometown__icontains=search) |
                Q(company__name__icontains=search)
            )
        
        return queryset

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Thống kê chiến sỹ"""
        total_soldiers = Soldier.objects.count()
        total_companies = Company.objects.count()
        
        # Thống kê theo đại đội
        companies_stats = []
        for company in Company.objects.all():
            companies_stats.append({
                'company_id': company.id,
                'company_name': company.name,
                'soldiers_count': company.soldiers.count()
            })
        
        return Response({
            'total_soldiers': total_soldiers,
            'total_companies': total_companies,
            'companies_stats': companies_stats
        }) 