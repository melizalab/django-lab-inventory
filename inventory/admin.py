from django.contrib import admin
from inventory.models import Item, Category, Unit, Manufacturer, Vendor, PTAO, Order

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = Order.items.through


class ItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'

    fieldsets = [
        (None, {'fields': ['name', 'chem_formula']}),
        ('Vendor Information', {'fields': ['vendor', 'catalog', 'manufacturer',
                                           'manufacturer_number',
                                           'size', 'unit',]}),
        ('Order Information', {'fields': [ 'units_purchased', 'cost', 'category']}),
        ('Item Information', {'fields': ['date_arrived', 'serial', 'uva_equip',
                                         'location', 'expiry_years', 'parent_item']}),
        (None, {'fields': ['comments']})
    ]

    list_display = ('name', 'category', 'date_added', 'date_arrived', 'total_price', 'location')
    list_filter = ('category', 'vendor', 'manufacturer', 'date_added', 'date_arrived')
    search_fields = ('name', 'chem_formula', 'serial', 'manufacturer_number', 'comments')
    inlines = [
        OrderItemInline,
    ]

admin.site.register(Item, ItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'order_date'
    fields = ('name', 'order_date', 'ordered_by', 'ordered', 'ptao', 'reconciled')
    list_display = ('name', 'item_count', 'order_date', 'ordered', 'reconciled', 'ptao')
    list_filter = ('ordered', 'reconciled', 'ptao', 'ordered_by')
    search_fields = ('name',)
    inlines = [
        OrderItemInline,
    ]

admin.site.register(Order, OrderAdmin)


class PTAOAdmin(admin.ModelAdmin):
    fields = list_display = ('code', 'description')


admin.site.register(PTAO, PTAOAdmin)

for model in (Category, Unit, Manufacturer, Vendor):
    admin.site.register(model)
