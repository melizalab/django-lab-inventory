from django.contrib import admin

from inventory.models import (
    Account,
    Category,
    Item,
    Manufacturer,
    Order,
    OrderAccount,
    OrderItem,
    Unit,
    Vendor,
)

from django.contrib import admin
from .models import StockItem, CheckoutRecord
from django.utils.html import format_html
import qrcode, io, base64

@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('name','sku','qr_token','qr_image')
    readonly_fields = ('qr_token','qr_image')

    def qr_image(self, obj):
        if not obj or not obj.qr_token:
            return ''
        qr = qrcode.make(str(obj.qr_token))
        buf = io.BytesIO(); qr.save(buf, format='PNG')
        data = base64.b64encode(buf.getvalue()).decode('ascii')
        return format_html('<img src="data:image/png;base64,{}" width="120" />', data)
    qr_image.short_description = 'QR'

@admin.register(CheckoutRecord)
class CheckoutRecordAdmin(admin.ModelAdmin):
    list_display = ('item','student','status','checked_out_at','due_date','returned_at')
    list_filter = ('status',)


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1


class OrderAccountInline(admin.StackedInline):
    model = OrderAccount
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"

    fieldsets = [
        (None, {"fields": ["name", "chem_formula", "category"]}),
        (
            "Vendor Information",
            {
                "fields": [
                    "vendor",
                    "catalog",
                    "manufacturer",
                    "manufacturer_number",
                    "size",
                    "unit",
                ]
            },
        ),
        (None, {"fields": ["parent_item", "comments"]}),
    ]

    list_display = (
        "name",
        "category",
        "vendor",
        "catalog",
        "created_at",
    )
    list_filter = ("category", "vendor", "manufacturer", "created_at")
    search_fields = ("name", "chem_formula", "manufacturer_number", "comments")
    inlines = (OrderItemInline,)


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = "placed_on"
    fields = (
        "name",
        "placed_on",
        "requested_by",
    )
    list_display = ("name", "placed_on", "display_accounts")
    list_filter = ("accounts", "requested_by")
    search_fields = ("name",)
    inlines = (OrderItemInline, OrderAccountInline)

    def display_accounts(self, obj):
        return ", ".join([acc.code for acc in obj.accounts.all()])

    display_accounts.short_description = "Accounts"


class OrderItemAdmin(admin.ModelAdmin):
    date_hierarchy = "arrived_on"
    fields = (
        "units_purchased",
        "cost",
        "arrived_on",
        "serial",
        "uva_equip",
        "location",
        "expiry_years",
        "reconciled",
    )
    list_display = ("name", "ordered_on", "arrived_on", "total_cost", "location")
    list_filter = ("item__name", "location")


class AccountAdmin(admin.ModelAdmin):
    fields = ("code", "description", "expires_on")
    list_display = fields


admin.site.register(Item, ItemAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

for model in (Category, Unit, Manufacturer, Vendor):
    admin.site.register(model)
