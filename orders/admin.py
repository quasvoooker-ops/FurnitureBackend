from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'total', 'created_at']
    list_filter = ['status']
    search_fields = ['customer__email', 'customer__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
