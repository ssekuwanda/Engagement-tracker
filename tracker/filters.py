from tracker.models import Engagement
import django_filters
from django import forms

class EngagementFilter(django_filters.FilterSet):
    class Meta:
        model = Engagement
        fields = ['year','assignment','currency','type','client']
