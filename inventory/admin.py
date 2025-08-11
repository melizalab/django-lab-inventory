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
