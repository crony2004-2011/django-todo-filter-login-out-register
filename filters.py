import django_filters

from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ['assign']

#this filter will only filter title column of the task model