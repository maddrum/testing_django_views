from django.shortcuts import render
from django.views.generic import ListView

from apps.working_times.models import WorkingTime


# Create your views here.
class WorkingTimesListView(ListView):
    model = WorkingTime
    template_name = "working_times/list.html"
    paginate_by = 10
