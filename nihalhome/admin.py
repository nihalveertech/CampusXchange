from django.contrib import admin
from .models import Item, Transaction


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seller', 'price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'seller__username')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'buyer', 'seller', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('item__title', 'buyer__username', 'seller__username')