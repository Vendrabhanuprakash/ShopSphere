from django.contrib import admin
from .models import (
    Category,
    Product,
    CustomerProfile,
    Cart,
    CartItem,
    Order,
    OrderItem
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name'
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'price',
        'stock'
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'name',
    )

    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'phone'
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'created_at'
    )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'cart',
        'product',
        'quantity'
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'total_amount',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price'
    )