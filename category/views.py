from django.shortcuts import render
from django.views.generic import DateDetailView
from .models import Category


class CategoryDetailView(DateDetailView):
    model = Category
    template_name = 'Category/detail.html'
    context_object_name = 'category'
