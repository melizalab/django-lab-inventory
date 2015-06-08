# -*- coding: utf-8 -*-
# -*- mode: python -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
import datetime

class Item(models.Model):
    name = models.CharField(max_length=128)
    chem_formula = models.CharField('Chemical formula', max_length=45,
                                    blank=True, null=True)

    vendor = models.ForeignKey('Vendor')
    catalog = models.CharField('Catalog number', max_length=45,
                               blank=True, null=True)
    manufacturer = models.ForeignKey('Manufacturer', blank=True, null=True)
    manufacturer_number = models.CharField(max_length=45,
                                           blank=True, null=True)
    size = models.DecimalField('Size of unit',
                               max_digits=10, decimal_places=2,
                               blank=True, null=True)
    unit = models.ForeignKey('Unit')
    units_purchased = models.IntegerField()
    cost = models.DecimalField('Cost per unit', max_digits=10, decimal_places=2,
                               blank=True, null=True)
    category = models.ForeignKey('Category')
    date_added = models.DateField(auto_now_add=True)
    date_arrived = models.DateField(blank=True, null=True)
    serial = models.CharField('Serial number', max_length=45,
                              blank=True, null=True)
    uva_equip = models.CharField('UVa equipment number', max_length=32,
                                 blank=True, null=True)
    location = models.CharField(max_length=45,
                                blank=True, null=True)
    parent_item = models.ForeignKey('self', blank=True, null=True)
    expiry_years = models.DecimalField('Warranty or Item expiration (y)', max_digits=4,
                                       decimal_places=2, blank=True, null=True)
    comments = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def unit_size(self):
        return "%s%s%s" % (self.size or "",
                           "" if str(self.unit).startswith("/") else " ",
                           self.unit)

    def total_price(self):
        return (self.cost or 0) * self.units_purchased

    def get_absolute_url(self):
        return reverse("inventory:item", kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=45)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']


class Unit(models.Model):
    name = models.CharField(max_length=45)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Manufacturer(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=64, blank=True, null=True)
    rep = models.CharField(max_length=45, blank=True, null=True)
    rep_phone = models.CharField(max_length=16, blank=True, null=True)
    support_phone = models.CharField(max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Vendor(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=16, blank=True, null=True)
    rep = models.CharField(max_length=45, blank=True, null=True)
    rep_phone = models.CharField(max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PTAO(models.Model):
    code = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    expires = models.DateField(blank=True, null=True)

    def active(self):
        return datetime.date.today() < self.expires

    def __unicode__(self):
        return "%s (%s)" % (self.code, self.description)

    class Meta:
        ordering = ['code']
        verbose_name = "PTAO"
        verbose_name_plural = "PTAOs"


class Order(models.Model):
    name = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField('Item', blank=True)
    ptao = models.ForeignKey(PTAO, blank=True, null=True)
    ordered = models.BooleanField()
    order_date = models.DateField(default=datetime.date.today)
    ordered_by = models.ForeignKey(User)
    reconciled = models.BooleanField()

    def __unicode__(self):
        if self.ordered:
            status = self.order_date
        else:
            status = "in progress"
        return "%s (%s)" % (self.name, status)

    @property
    def item_count(self):
        return self.items.count

    def get_absolute_url(self):
        return reverse("inventory:order", kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-order_date', 'name']
