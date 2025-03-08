from django.conf.urls.i18n import set_language
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("diary.urls")),  # Маршруты для приложения diary
    path("accounts/", include("accounts.urls")),  # Маршруты для приложения accounts
    path("set_language/", set_language, name="set_language"),
]
