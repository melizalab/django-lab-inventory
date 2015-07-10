from django.contrib import admin
from inventory.models import Item, Category, Unit, Manufacturer, Vendor, PTAO, Order, OrderItem

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'

    fieldsets = [
        (None, {'fields': ['name', 'chem_formula', 'category']}),
        ('Vendor Information', {'fields': ['vendor', 'catalog', 'manufacturer',
                                           'manufacturer_number',
                                           'size', 'unit',]}),
        (None, {'fields': ['parent_item', 'comments']})
    ]

    list_display = ('name', 'category', 'date_added',)
    list_filter = ('category', 'vendor', 'manufacturer', 'date_added')
    search_fields = ('name', 'chem_formula', 'manufacturer_number', 'comments')
    inlines = (OrderItemInline,)

admin.site.register(Item, ItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'order_date'
    fields = ('name', 'order_date', 'ordered_by', 'ordered', 'ptao',)
    list_display = ('name', 'item_count', 'order_date', 'ordered', 'ptao')
    list_filter = ('ordered', 'ptao', 'ordered_by')
    search_fields = ('name',)
    inlines = (OrderItemInline,)

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_arrived'
    fields = ('units_purchased', 'cost', 'date_arrived', 'serial', 'uva_equip',
              'location', 'expiry_years', 'reconciled')
    list_display = ('name', 'order_date', 'date_arrived', 'total_price', 'location')
    list_filter = ('item__name', 'order__order_date', 'date_arrived', 'location')

admin.site.register(OrderItem, OrderItemAdmin)

class PTAOAdmin(admin.ModelAdmin):
    fields = ('code', 'description', 'expires')
    list_display = fields + ('active',)


admin.site.register(PTAO, PTAOAdmin)

for model in (Category, Unit, Manufacturer, Vendor):
    admin.site.register(model)
