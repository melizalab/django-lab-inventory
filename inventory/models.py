# -*- coding: utf-8 -*-
# -*- mode: python -*-
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, F, Q, Sum
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
    expires_on = models.DateField(blank=True, null=True)

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
    created_at = models.DateTimeField(auto_now_add=True)
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
        space = "" if str(self.unit).startswith("/") else " "
        return f"{self.size or ''}{space}{self.unit}"

    def vendor_url(self):
        try:
            return self.vendor.lookup_url % self.catalog
        except (ValueError, AttributeError, TypeError):
            return None

    def mfg_url(self):
        try:
            return self.manufacturer.lookup_url % self.manufacturer_number
        except (ValueError, AttributeError, TypeError):
            return None

    def get_absolute_url(self):
        return reverse("inventory:item", kwargs={"pk": self.pk})

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["vendor", "catalog"], name="unique_vendor_catalog_number"
            )
        ]


class OrderQuerySet(models.QuerySet):
    def with_counts(self, on_date: datetime.date | None = None):
        on_date = on_date or datetime.date.today()
        return self.annotate(
            item_count=Count("orderitem"),
            item_received_count=Count(
                "orderitem", filter=Q(orderitem__arrived_on__lte=on_date)
            ),
        )

    def placed(self, on_date: datetime.date | None = None):
        return self.filter(placed_on__lte=on_date or datetime.date.today())

    def not_placed(self, on_date: datetime.date | None = None):
        return self.exclude(placed_on__lte=on_date or datetime.date.today())

    def completed(self, on_date: datetime.date | None = None):
        return (
            self.placed()
            .with_counts(on_date)
            .filter(item_count=F("item_received_count"))
        )

    def not_completed(self, on_date: datetime.date | None = None):
        return (
            self.placed()
            .with_counts(on_date)
            .filter(item_count__gt=F("item_received_count"))
        )


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, through="OrderItem")
    accounts = models.ManyToManyField(
        Account, through="OrderAccount", blank=True, related_name="orders"
    )
    placed_on = models.DateField(blank=True, null=True)
    requested_by = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name="Requested by"
    )
    objects = OrderQuerySet.as_manager()

    def __str__(self):
        status = self.placed_on or "in progress"
        return f"{self.name} ({status})"

    def get_absolute_url(self):
        return reverse("inventory:order", kwargs={"pk": self.pk})

    def total_cost(self):
        totals = self.orderitem_set.with_totals().aggregate(
            Sum("total_cost", default=0)
        )
        return totals["total_cost__sum"]

    def mark_placed(self, on_date: datetime.date | None = None):
        self.placed_on = on_date or datetime.date.today()
        self.save()

    def add_item(self, item: Item, n_units: int, cost_per_unit: float) -> "OrderItem":
        return OrderItem.objects.create(
            item=item, order=self, units_purchased=n_units, cost=cost_per_unit
        )

    def add_account(self, account: Account) -> "OrderAccount":
        return OrderAccount.objects.create(order=self, account=account)

    def account_codes(self) -> str:
        return ", ".join(acct.code for acct in self.accounts.all())

    def account_descriptions(self) -> str:
        return ", ".join(str(acct) for acct in self.accounts.all())

    class Meta:
        ordering = ["-created_at"]


class OrderItemQuerySet(models.QuerySet):
    def with_totals(self):
        return self.annotate(total_cost=F("cost") * F("units_purchased"))


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    units_purchased = models.IntegerField()
    cost = models.DecimalField(
        "Cost per unit", max_digits=10, decimal_places=2, blank=True, null=True
    )

    arrived_on = models.DateField(blank=True, null=True)
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

    objects = OrderItemQuerySet.as_manager()

    def total_cost(self):
        return (self.cost or 0) * self.units_purchased

    def name(self):
        return self.item.name

    def ordered_on(self):
        return self.order.placed_on

    def __str__(self):
        return f"{self.name()} [{self.ordered_on()}]"

    def mark_arrived(self, on_date: datetime.date | None = None):
        self.arrived_on = on_date or datetime.date.today()
        self.save()

    class Meta:
        db_table = "inventory_order_items"


class OrderAccount(models.Model):
    """
    Through model for Order-Account relationship.
    Allows for future additions like allocation percentages, notes, etc.
    """

    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Future fields can be added here without changing the relationship structure
    # e.g., allocation_percentage, notes, etc.

    class Meta:
        db_table = "inventory_order_accounts"
        unique_together = ["order", "account"]
        ordering = ["account__code"]

    def __str__(self):
        return f"{self.order.name} - {self.account.code}"
