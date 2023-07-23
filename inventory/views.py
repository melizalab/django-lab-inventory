# -*- coding: utf-8 -*-
# -*- mode: python -*-
from django.shortcuts import get_object_or_404, redirect
import django_filters as filters
from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from django_filters.views import FilterView

from inventory.models import Item, Order
from inventory.forms import NewOrderForm, NewItemForm, NewOrderItemForm


def index(request):
    return render(request, "inventory/index.html")


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
    ordered_by = filters.CharFilter(
        field_name="ordered_by__username", lookup_expr="istartswith", label="Ordered by"
    )
    account = filters.CharFilter(
        field_name="account__description", lookup_expr="icontains", label="Account"
    )
    # example of a drop-down filter. I don't like how these look though
    # ordered_by = filters.ModelChoiceFilter(
    #     field_name="ordered_by",
    #     queryset=User.objects.all(),
    #     label="User",
    #     to_field_name="username",
    # )

    class Meta:
        model = Order
        fields = ["name", "ordered_by", "account"]


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
        field_name="category__name", lookup_expr="istartswith", label="Category"
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
        model = Order
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


class OrderView(generic.DetailView):
    model = Order
    template_name = "inventory/order.html"

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context["orderitem_list"] = context["order"].orderitem_set.order_by(
            "item__vendor"
        )
        return context


class OrderEntry(generic.FormView):
    template_name = "inventory/order_entry.html"
    form_class = NewOrderForm

    def get_initial(self):
        initial = super().get_initial()
        initial["ordered_by"] = self.request.user
        return initial

    def form_valid(self, form):
        order = form.save(commit=False)
        order.ordered = False
        order.save()
        return redirect("inventory:order", pk=order.id)


class ItemList(PaginatedFilterView):
    model = Item
    filterset_class = ItemFilter
    template_name = "inventory/item_list.html"
    context_object_name = "item_list"

    def get_queryset(self):
        qs = Item.objects.filter(**self.kwargs)
        return qs.order_by("-date_added")


class ItemView(generic.DetailView, generic.FormView):
    model = Item
    template_name = "inventory/item.html"
    form_class = NewOrderItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lineitems"] = context["item"].orderitem_set.order_by(
            "-order__order_date"
        )
        return context


class ItemEntry(generic.FormView):
    template_name = "inventory/item_entry.html"
    form_class = NewItemForm

    def form_valid(self, form):
        item = form.save()
        return redirect("inventory:item", pk=item.id)


class OrderItemEntry(generic.FormView):
    """Order an item (associate it with an order)"""

    template_name = "inventory/orderitem_entry.html"
    form_class = NewOrderItemForm

    def form_valid(self, form):
        item_id = self.kwargs["pk"]
        form.instance.item = get_object_or_404(Item, pk=item_id)
        form.instance.reconciled = False
        oitem = form.save()
        return redirect("inventory:order", pk=oitem.order.id)
