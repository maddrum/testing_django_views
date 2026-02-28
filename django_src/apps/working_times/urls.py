from django.urls import path
import apps.working_times.views as views

urlpatterns = [
    path("", views.WorkingTimesListView.as_view(), name="working_times_list"),
]
