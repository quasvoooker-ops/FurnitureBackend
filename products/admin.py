from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
