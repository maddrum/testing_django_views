from django.contrib import admin

from apps.working_times.models import WorkingTime


class WorkingTimeAdmin(admin.ModelAdmin):
    list_display = ("shop_name", "from_time", "to_time", "note")
    list_filter = ("shop_name",)
    search_fields = ("shop_name",)


admin.site.register(WorkingTime, WorkingTimeAdmin)
