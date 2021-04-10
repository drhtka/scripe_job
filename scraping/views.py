# -*- coding: utf-8 -*-
from .models import Vacancy
from .forms import FindForm
from django.shortcuts import render

def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    qs = []
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city # так как foregin key извлекаем класс city потом поле slug и создаем словарь
        if language:
            _filter['language__slug'] = language

        qs = Vacancy.objects.filter(**_filter)
    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})
