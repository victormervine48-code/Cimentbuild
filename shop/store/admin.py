from django.contrib import admin
from .models import Category, Product, Order, OrderItem, DeliveryZone, Supplier, Driver, StockMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "purchase_price", "unit", "stock", "active")
    list_filter = ("category", "active", "supplier")
    search_fields = ("name", "description")

@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "fee", "active")

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "active")

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "vehicle", "active")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("unit_price",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "phone", "status", "payment_method", "payment_status", "driver", "created_at")
    list_filter = ("status", "payment_method", "payment_status", "zone")
    search_fields = ("customer_name", "phone", "address")
    inlines = [OrderItemInline]

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "movement_type", "quantity", "reason", "created_at")
    list_filter = ("movement_type",)
