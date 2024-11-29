from django.contrib import admin
from .models import ShimlaAttraction

@admin.register(ShimlaAttraction)
class ShimlaAttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'opening_hours')
    search_fields = ('name', 'location')
