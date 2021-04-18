# -*- coding: utf-8 -*-
import asyncio

import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint
# 51 less scripe_job подкл django settings
import os, sys
from bs4 import BeautifulSoup as BS
from random import randint

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))  # абсолютный путь 8 мин 51 less
sys.path.append(proj)  # добавить в системные переменные путей
os.environ[
    "DJANGO_SETTINGS_MODULE"] = 'scripe_job.settings'  # будет установлена в переменных окружения, указываем название проекта где файл settings.py

import django

django.setup()
# 52 less scripe_job подкл django settings end
from scraping.parsers import *  # импрортим все
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()  # вернет того пользователя который опрделён в рамках нашего джанго проекта
#
# parsers = (
#     (work, 'https://www.work.ua/ru/jobs-kyiv-python'),
#     (dou, 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'),
#     (djinni, 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'),
#     (rabota, 'https://rabota.ua/zapros/python/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0'),
# )

parsers = ( # будем подставлят урл из словаря
    (work, 'work'),
    (dou, 'dou'),
    (djinni, 'djinni'),
    (rabota, 'rabota'),
)
jobs, errors = [], []
def get_settings():
    qs = User.objects.filter(send_email=True).values()# т.е мы используем не MyUser, User того ког определила джанго
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)# получим айдишники из кверисет city_id'], q['language_id
    # print(settings_lst)
    return settings_lst

def get_urls(_settings): # на вход будем получать данные из get_settings()
    # нам необходимо получтиь те наборы из базы которые мы будем использовать
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}# преобразовываем qs в словарь позволит нам создать набор урлов для дальнейшего испоьзования в функции
    urls = []

    for pair in _settings: # _settings  {(1, 1)}
        tmp = {}
        tmp['city'] = pair[0] #'city': 1,
        tmp['language'] = pair[1] # 'language': 1,
        # url_data = url_dict.get(pair)
        tmp['url_data'] = url_dict[pair] # {'work': 'https://www.work.ua/ru/jobs-kyiv-python', 'rabota': 'https://rabota.ua/zapros/python/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0', 'dou': 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python', 'djinni': 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'}
        urls.append(tmp) # [{'city': 1, 'language': 1, 'url_data': {'work': 'https://www.work.ua/ru/jobs-kyiv-python', 'rabota': 'https://rabota.ua/zapros/python/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0', 'dou': 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python', 'djinni': 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'}}]
    return urls
async def main(value):
    func, url, city, language = value # таким образом мы получаем значения запакованные tmp_tasks =  [(func, data['url_data'][key], data['city'], data['language'])
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err) #  в асинхронном режиме запкскаем в соотвествующие сиски
    jobs.extend(job) #   в асинхронном режиме запкскаем в соотвествующие сиски

settings = get_settings()
url_list = get_urls(settings)

# city = City.objects.filter(slug='kiev').first()
# language = Language.objects.filter(slug='python').first()

# print(city)
# print(language)
# import time  1

# start = time.time()  2
loop = asyncio.get_event_loop()# создаем некиц loop в котором будет запускаться наша задача, необходимо создать задачи потом выполнить
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language']) # - название функции, data['url_data'][key]  url
             for data in url_list
             for func, key in parsers]

tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])

#
# for data in url_list:
#
#     for func, key in parsers:
#         # print(func, url)
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e

loop.run_until_complete(tasks)
loop.close()
#print(time.time()-start)# 3 узнаем сколько времени ушло на ваполнениние запроса

for job in jobs:
    v = Vacancy(**job)  # раскрываем словарь,
    try:
        v.save()  # и записвыаем в базу данных
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()
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
