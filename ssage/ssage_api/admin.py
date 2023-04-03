from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Order, Supply
# Register your models here.


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('productName', 'productCode', 'stock', 'location',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('productName', 'productCode', 'total',)


class OrderInline(admin.TabularInline):
    model = Order.user.through
    extra = 1


class CustomUserAdmin(UserAdmin):
    inlines = [OrderInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
