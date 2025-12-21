# -*- coding: utf-8 -*-
# -*- mode: python -*-
import django_filters as filters
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views import generic
from django_filters.views import FilterView
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import StockItem, CheckoutRecord
from django.http import HttpResponse
import csv

@login_required
def quick_checkout(request, token):
    item = get_object_or_404(StockItem, qr_token=token)
    if request.method == 'POST':
        try:
            due_days = int(request.POST.get('due_days', 7))
        except (ValueError, TypeError):
            due_days = 7
        due_date = timezone.now() + timezone.timedelta(days=due_days)
        co = CheckoutRecord.objects.create(item=item, student=request.user, due_date=due_date, status='out')
        return render(request, 'inventory/quick_checkout_success.html', {'checkout': co})
    return render(request, 'inventory/quick_checkout.html', {'item': item})


from inventory.forms import (
    ConfirmOrderForm,
    NewItemForm,
    NewOrderForm,
    NewOrderItemForm,
    OrderItemReceivedForm,
)
from inventory.models import Item, Order, OrderItem


@receiver(user_logged_in)
def clear_login_attempts(sender, request, user, **kwargs):
    """Clear failed login attempts on successful login"""
    from inventory.middleware import LoginAttemptMiddleware
    ip_address = request.META.get('REMOTE_ADDR')
    LoginAttemptMiddleware.clear_attempts(ip_address, user.username)


def index(request):
    stats = {
        "item_count": Item.objects.count(),
        "order_count": Order.objects.count(),
        "unplaced_count": Order.objects.not_placed().count(),
        "incomplete_count": Order.objects.not_completed().count(),
        "stock_item_count": StockItem.objects.count(),
        "active_checkouts": CheckoutRecord.objects.filter(status='out').count(),
    }
    recent_orders = Order.objects.with_counts().order_by("-created_at")[:5]
    recent_items = Item.objects.order_by("-created_at")[:5]
    recent_stock_items = StockItem.objects.all()[:6]
    recent_checkouts = CheckoutRecord.objects.select_related('item', 'student').order_by("-checked_out_at")[:5]
    
    return TemplateResponse(
        request,
        "inventory/index.html",
        {
            "stats": stats, 
            "recent_orders": recent_orders, 
            "recent_items": recent_items,
            "recent_stock_items": recent_stock_items,
            "recent_checkouts": recent_checkouts,
        },
    )


class PaginatedFilterView(FilterView):
    paginate_by = 25

    def get_context_data(self, **kwargs):
        # This strips the page from the query parameters; otherwise pagination leads to ever-growing URL
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.copy()
        try:
            del context["query"]["page"]
        except KeyError:
            pass
        return context


class OrderFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains", label="Name")
    requested_by = filters.CharFilter(
        field_name="requested_by__username",
        lookup_expr="istartswith",
        label="Placed by",
    )
    account = filters.CharFilter(
        field_name="accounts__description", lookup_expr="icontains", label="Account"
    )

    class Meta:
        model = Order
        fields = ["name", "requested_by", "account"]


class ItemFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name="name", lookup_expr="icontains", label="Description"
    )
    vendor_or_mfg = filters.CharFilter(
        method="by_vendor_or_mfg", label="Vendor/Manufacturer"
    )
    catalog_or_part = filters.CharFilter(
        method="by_catalog_or_part", label="Catalog/Part Number"
    )
    category = filters.CharFilter(
        field_name="category__name", lookup_expr="icontains", label="Category"
    )

    def by_vendor_or_mfg(self, queryset, name, value):
        return queryset.filter(
            Q(vendor__name__icontains=value) | Q(manufacturer__name__icontains=value)
        )

    def by_catalog_or_part(self, queryset, name, value):
        return queryset.filter(
            Q(catalog__icontains=value) | Q(manufacturer_number__icontains=value)
        )

    class Meta:
        model = Item
        fields = [
            "name",
            "vendor_or_mfg",
            "catalog_or_part",
            "category",
        ]


class OrderList(PaginatedFilterView):
    model = Order
    filterset_class = OrderFilter
    template_name = "inventory/order_list.html"
    context_object_name = "order_list"

    def get_queryset(self):
        qs = Order.objects.with_counts().filter(**self.kwargs)
        return qs.order_by("-created_at")


class UnplacedOrderList(OrderList):
    def get_queryset(self):
        qs = Order.objects.with_counts().not_placed().filter(**self.kwargs)
        return qs.order_by("-created_at")


class IncompleteOrderList(OrderList):
    def get_queryset(self):
        qs = Order.objects.with_counts().not_completed().filter(**self.kwargs)
        return qs.order_by("-created_at")


class OrderView(generic.DetailView):
    model = Order
    template_name = "inventory/order.html"

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context["orderitem_list"] = context["order"].orderitem_set.order_by(
            "item__vendor"
        )
        return context


def order_entry(request):
    if request.method == "POST":
        form = NewOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect("inventory:order", pk=order.id)
    else:
        form = NewOrderForm(initial={"requested_by": request.user})
    return TemplateResponse(request, "inventory/order_entry.html", {"form": form})


def mark_order_placed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        form = ConfirmOrderForm(request.POST, instance=order)
        if form.is_valid():
            # order = form.save(commit=False)
            order.mark_placed()
            return redirect("inventory:order", pk=order_id)
    else:
        form = ConfirmOrderForm(instance=order)
    return TemplateResponse(
        request, "inventory/order_mark_placed.html", {"order": order, "form": form}
    )


def mark_orderitem_received(request, orderitem_id):
    orderitem = get_object_or_404(OrderItem, id=orderitem_id)
    if request.method == "POST":
        form = OrderItemReceivedForm(request.POST, instance=orderitem)
        if form.is_valid():
            orderitem.mark_arrived(form.cleaned_data["arrived_on"])
            return redirect("inventory:order", pk=orderitem.order.id)
    else:
        form = OrderItemReceivedForm(instance=orderitem)
    return TemplateResponse(
        request,
        "inventory/orderitem_mark_received.html",
        {"orderitem": orderitem, "form": form},
    )


class ItemList(PaginatedFilterView):
    model = Item
    filterset_class = ItemFilter
    template_name = "inventory/item_list.html"
    context_object_name = "item_list"

    def get_queryset(self):
        qs = Item.objects.filter(**self.kwargs)
        return qs.order_by("-created_at")


@login_required
def export_items_csv(request):
    """Export items as CSV. Respects the same filter query params as the list view."""
    # Apply the same filters as ItemList so users can export filtered results
    f = ItemFilter(request.GET, queryset=Item.objects.all())
    qs = f.qs.order_by("-created_at")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="inventory_items.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Description",
        "Unit",
        "Vendor",
        "Catalog number",
        "Manufacturer",
        "Part Number",
        "Category",
    ])

    for item in qs:
        writer.writerow([
            item.name,
            item.unit_size or "",
            str(item.vendor) if getattr(item, "vendor", None) else "",
            item.catalog or "",
            str(item.manufacturer) if getattr(item, "manufacturer", None) else "",
            item.manufacturer_number or "",
            str(item.category) if getattr(item, "category", None) else "",
        ])

    return response


class ItemView(generic.DetailView, generic.FormView):
    model = Item
    template_name = "inventory/item.html"
    form_class = NewOrderItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lineitems"] = context["item"].orderitem_set.order_by(
            "-order__placed_on"
        )
        return context


def item_entry(request):
    if request.method == "POST":
        form = NewItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect("inventory:item", pk=item.id)
    else:
        form = NewItemForm()
    return TemplateResponse(request, "inventory/item_entry.html", {"form": form})


def item_copy(request, item_id):
    """Make a copy of an item - populates the form with existing values"""
    if request.method == "POST":
        form = NewItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect("inventory:item", pk=item.id)
    else:
        original_item = get_object_or_404(Item, id=item_id)
        initial_data = {}
        for field_name in NewItemForm.Meta.fields:
            if hasattr(original_item, field_name):
                value = getattr(original_item, field_name)
                initial_data[field_name] = value

        # Modify the name to indicate it's a copy
        initial_data["name"] = f"Copy of {original_item.name}"
        form = NewItemForm(initial=initial_data)
    return TemplateResponse(request, "inventory/item_entry.html", {"form": form})


def order_item_entry(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Item, id=item_id)
        form = NewOrderItemForm(request.POST)
        if form.is_valid():
            oitem = form.save(commit=False)
            oitem.item = item
            oitem.save()
            return redirect("inventory:order", pk=oitem.order.id)
        return TemplateResponse(
            request, "inventory/item.html", {"item": item, "form": form}
        )


class OrderItemDelete(generic.DeleteView):
    model = OrderItem
    template_name = "inventory/orderitem_confirm_delete.html"
    success_url = "/inventory/orders/{order_id}/"
