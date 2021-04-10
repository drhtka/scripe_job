# -*- coding: utf-8 -*-
from .models import Vacancy
from django.shortcuts import render

def home_view(request):
    qs = Vacancy.objects.all()
    return render(request, 'scraping/home.html', {'object_list': qs})
