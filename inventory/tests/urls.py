from django.contrib import admin
from django.contrib.auth import views as authviews
from django.urls import include, re_path
from django.views.generic import RedirectView

urlpatterns = [
    re_path(r"^$", RedirectView.as_view(pattern_name="inventory:index", permanent=False)),
    re_path(r"^university-laboratory-system/", include("inventory.urls")),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^accounts/login/$", authviews.LoginView.as_view(), name="login"),
    re_path(r"^accounts/logout/$", authviews.LogoutView.as_view(), name="logout"),
]
