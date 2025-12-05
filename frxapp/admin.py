from django.contrib import admin
from .models import Product




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "created_at")
    list_filter = ( "created_at",)
    search_fields = ("name", "description")
    list_editable = ("price", "stock")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Product Info", {
            "fields": ( "name", "description", "image")
        }),
        ("Pricing & Stock", {
            "fields": ("price", "stock")
        }),

    )
