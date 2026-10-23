from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_id', 'name', 'price', 'quantity', 'image']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'status', 'total', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['full_name', 'email']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at', 'subtotal', 'shipping_fee', 'total']

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
