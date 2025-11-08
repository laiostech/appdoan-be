from django.contrib import admin
from .models import Company, Soldier

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']

@admin.register(Soldier)
class SoldierAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company', 'soldier_rank', 'soldier_position', 'place_work', 'birth_date', 'phone_number']
    search_fields = ['full_name', 'soldier_rank', 'soldier_position', 'place_work', 'phone_number', 'hometown']
    list_filter = ['company', 'soldier_rank', 'soldier_position', 'place_work', 'ethnicity', 'education']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company', 'full_name', 'birth_date', 'soldier_rank', 'soldier_position', 'place_work')
        }),
        ('Union/Party Information', {
            'fields': ('join_union_party_date',)
        }),
        ('Personal Information', {
            'fields': ('ethnicity', 'education', 'religion', 'hometown', 'father_name', 'mother_name', 'phone_number')
        }),
        ('System Information', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ) 