# -*- coding: utf-8 -*-
import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint
# 51 less scripe_job подкл django settings
import os, sys
from bs4 import BeautifulSoup as BS
from random import randint

from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))# абсолютный путь 8 мин 51 less
sys.path.append(proj) # добавить в системные переменные путей
os.environ["DJANGO_SETTINGS_MODULE"] = 'scripe_job.settings' # будет установлена в переменных окружения, указываем название проекта где файл settings.py

import django
django.setup()
# 52 less scripe_job подкл django settings end
from scraping.parsers import * # импрортим все
from scraping.models import Vacancy, City, Language

parsers = (
    (work, 'https://www.work.ua/ru/jobs-kyiv-python'),
    (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
    (djinni, 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'),
    (rabota, 'https://rabota.ua/zapros/python/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0'),
)

city = City.objects.filter(slug='kiev').first()
language = Language.objects.filter(slug='python').first()

# print(city)
# print(language)
jobs, errors = [], []
for func, url in parsers:
    # print(func, url)
    j, e = func(url)
    jobs += j
    errors += e


for job in jobs:
    v = Vacancy(**job, city=city, language=language)# раскрываем словарь, фильруем по city langvuage выборки и записвыаем в базу данных
    try:
        v.save()
    except DatabaseError:
        pass
# 52 урок закоментили
# h = codecs.open('work.txt', 'w', 'utf-8')# открываем в режиме записи и задаем кодировку 'utf-8'
# h.write(str(jobs))# записываем весь контент словарем
# h.close()

# jobs, errors = [], []
# for func, key in parsers:
#     url = data['url_data'][key]
#     j, e = func(url, city=data['city'], language=data['language'])
#     jobs += j
#     errors += e
