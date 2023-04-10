from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Order, Supply, Message
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




class MessageInline(admin.TabularInline):
    model = Message
    fields = ['content','recipient', 'timestamp', 'is_seen']
    readonly_fields = ['timestamp']
    extra = 0
    fk_name = 'sender'

class CustomUserAdmin(UserAdmin):
    inlines = [OrderInline, MessageInline]


# @admin.register(Conversation)
# class ConversationAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user1', 'user2')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# admin.site.register(Message, MessageAdmin)