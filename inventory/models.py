# -*- coding: utf-8 -*-
# -*- mode: python -*-
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]


class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    url = models.CharField(max_length=64, blank=True, null=True)
    lookup_url = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        help_text="url pattern to look up part number",
    )
    rep = models.CharField(max_length=128, blank=True, null=True)
    rep_phone = models.CharField(max_length=16, blank=True, null=True)
    rep_email = models.CharField(max_length=64, blank=True, null=True)
    support_phone = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    url = models.CharField(max_length=64, blank=True, null=True)
    lookup_url = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="url pattern to look up catalog number",
    )
    phone = models.CharField(max_length=16, blank=True, null=True)
    rep = models.CharField(max_length=45, blank=True, null=True)
    rep_phone = models.CharField(max_length=16, blank=True, null=True)
    rep_email = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    expires = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s (%s)" % (self.description, self.code)

    class Meta:
        ordering = ["code"]
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    chem_formula = models.CharField(
        "Chemical formula", max_length=45, blank=True, null=True
    )

    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    catalog = models.CharField("Catalog number", max_length=45, blank=True, null=True)
    manufacturer = models.ForeignKey(
        "Manufacturer",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="leave blank if unknown or same as vendor",
    )
    manufacturer_number = models.CharField(max_length=45, blank=True, null=True)
    size = models.DecimalField(
        "Size of unit", max_digits=10, decimal_places=2, blank=True, null=True
    )
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    date_added = models.DateField(auto_now_add=True)
    parent_item = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="example: for printer cartriges, select printer",
    )
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def unit_size(self):
        if self.unit.name == "each":
            return self.unit.name
        return "%s%s%s" % (
            self.size or "",
            "" if str(self.unit).startswith("/") else " ",
            self.unit,
        )

    def total_price(self):
        return (self.cost or 0) * self.units_purchased

    def vendor_url(self):
        try:
            return self.vendor.lookup_url % self.catalog
        except (AttributeError, TypeError):
            return None

    def mfg_url(self):
        try:
            return self.manufacturer.lookup_url % self.manufacturer_number
        except (AttributeError, TypeError):
            return None

    def get_absolute_url(self):
        return reverse("inventory:item", kwargs={"pk": self.pk})

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vendor", "catalog"], name="unique_vendor_catalog_number"
            )
        ]


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, through="OrderItem")
    account = models.ForeignKey(
        Account, blank=True, null=True, on_delete=models.SET_NULL
    )
    ordered = models.BooleanField(default=False)
    order_date = models.DateField(default=datetime.date.today)
    ordered_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        if self.ordered:
            status = self.order_date
        else:
            status = "in progress"
        return "%s (%s)" % (self.name, status)

    @property
    def item_count(self):
        return self.items.count

    def get_absolute_url(self):
        return reverse("inventory:order", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created"]


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    units_purchased = models.IntegerField()
    cost = models.DecimalField(
        "Cost per unit", max_digits=10, decimal_places=2, blank=True, null=True
    )

    date_arrived = models.DateField(blank=True, null=True)
    serial = models.CharField("Serial number", max_length=45, blank=True, null=True)
    uva_equip = models.CharField(
        "UVa equipment number", max_length=32, blank=True, null=True
    )
    location = models.CharField(
        max_length=45,
        blank=True,
        null=True,
        help_text="example: -80 freezer, refrigerator, Gilmer 283",
    )
    expiry_years = models.DecimalField(
        "Warranty or Item expiration (y)",
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
    )

    reconciled = models.BooleanField(default=False)

    def total_price(self):
        return (self.cost or 0) * self.units_purchased

    def name(self):
        return self.item.name

    def order_date(self):
        return self.order.order_date

    def __str__(self):
        return "%s [%s]" % (self.item.name, self.order.order_date)

    class Meta:
        db_table = "inventory_order_items"
