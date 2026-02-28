from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("working-times/", include("apps.working_times.urls")),

]
