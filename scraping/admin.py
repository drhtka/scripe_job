# -*- coding: utf-8 -*-

from django.contrib import admin
from scraping.models import City, Language, Vacancy

admin.site.register(City)
admin.site.register(Language)
admin.site.register(Vacancy)
# Register your models here.
