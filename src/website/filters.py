import django_filters
from django.db.models import Q
from django.forms import TextInput

from src.website.models import Blog


class BlogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label=''
                                      , widget=TextInput(attrs={'placeholder': 'Search Posts here',
                                                                'class': 'form-control rounded-pill'}),
                                      method='post_filter')

    class Meta:
        model = Blog
        fields = ['title',]

    def post_filter(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))
