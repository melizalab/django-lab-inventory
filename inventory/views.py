# -*- coding: utf-8 -*-
# -*- mode: python -*-
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
import django_filters as filters
from django_filters.views import FilterView

from inventory.models import Order, Item


def index(request):
    return render(request, "inventory/index.html")


class OrderFilter(filters.FilterSet):
    ordered_by = filters.CharFilter(
        field_name="ordered_by__username", lookup_expr="istartswith"
    )
    account = filters.CharFilter(
        field_name="ptao__description", lookup_expr="icontains"
    )

    class Meta:
        model = Order
        fields = {"name": ["icontains"]}


class OrderList(FilterView):
    model = Order
    filterset_class = OrderFilter
    template_name = "inventory/order_list.html"
    context_object_name = "order_list"
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.copy()
        try:
            del context["query"]["page"]
        except KeyError:
            pass
        return context


class OrderView(generic.DetailView):
    model = Order
    template_name = "inventory/order.html"

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context["lineitems"] = context["order"].orderitem_set.order_by("item__vendor")
        return context


class ItemView(generic.DetailView):
    model = Item
    template_name = "inventory/item.html"

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context["lineitems"] = context["item"].orderitem_set.order_by(
            "order__order_date"
        )
        return context
