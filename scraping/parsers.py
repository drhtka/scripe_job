# -*- coding: utf-8 -*-
import requests
import codecs# и меняем сразу кодировку 'utf-8'
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('work', "rabota", 'dou', 'djinni') # импортируем только эти функции

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]

def work(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    # url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    if url: # 58 less
        resp = requests.get(url, headers=headers[randint(0, 2)]) # делаем запрос представишись браузером рендомно [randint(0, 2)] и что то вернет в ответ
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')# что парсим метод парсера html.parser
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_lst:
                        title = div.find('h2')
                        href = title.a['href'] # добираемся до  урл
                        content = div.p.text
                        company = 'No name'
                        logo = div.find('img')
                        if logo:# если мы находим img
                            company = logo['alt']# обращаемся к атрибуту алт
                        jobs.append({'title': title.text, 'url': domain + href,
                                    'description': content, 'company': company,
                                     'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Table does not exists"})
        else:
            errors.append({'url': url, 'title': "Page is empty"})

    return jobs, errors

def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    # url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)]) # делаем запрос представишись браузером и что то вернет в отвер
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')# что парсим метод парсера html.parser
            new_jobs = soup.find('div',
                                     attrs={'class': 'f-vacancylist-newnotfound'})
            if not new_jobs: # если нет такого класса запускаем всю логику
                table = soup.find('table', id='ctl00_content_vacancyList_gridList')
                if table:# если таблица есть
                    tr_lst = table.find_all('tr', attrs={'id': True})# тогда ищем tr, 'id': True значит айдишник есть
                    for tr in tr_lst:
                            div = tr.find('div', attrs={'class': 'card-body'})
                            if div:
                                title = div.find('h2',
                                                attrs={'class': 'card-title'})
                                href = title.a['href'] # добираемся до  урл
                                content = div.p.text
                                company = 'No name'
                                p = div.find('p', attrs={'class': 'company-name'})
                                if p:# если мы находим p
                                    try:
                                        company = p.a.text
                                    except AttributeError:
                                        print('111')
                                    # print('company')
                                    # print(p.a['title'])
                                jobs.append({'title': title.text,
                                             'url': domain + href,
                                             'description': content,
                                             'company': str(company),
                                             'city_id': city, 'language_id': language})
                else:
                    errors.append({'url': url, 'title': "Table does not exists"})
            else:
                errors.append({'url': url, 'title': "Page is empty"})
        else:
            errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors

def dou(url, city=None, language=None):
    jobs = []
    errors = []
    # domain = 'https://www.work.ua'
    # url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)]) # делаем запрос представишись брайзером и что то вернет в отвер
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')# что парсим метод парсера html.parser
            main_div = soup.find('div', id='vacancyListId')
            if main_div:
                li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
                for li in li_lst:
                        title = li.find('div', attrs={'class': 'title'})
                        href = title.a['href'] # добираемся до  урл
                        cont = li.find('div', attrs={'class': 'sh-info'})
                        content = cont.text
                        company = 'No name'
                        a = title.find('a', attrs={'class': 'company'})
                        if a:
                            company = a.text
                        jobs.append({'title': title.text, 'url': href, # домен не нужен ссылка абсолютная
                                    'description': content, 'company': company,
                                     'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Table does not exists"})
        else:
            errors.append({'url': url, 'title': "Page is empty"})

    return jobs, errors

def djinni(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://djinni.co'
    # url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)]) # делаем запрос представишись брайзером и что то вернет в отвер
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')# что парсим метод парсера html.parser
            main_ul = soup.find('ul', attrs={'class': "list-jobs"})# заходим в ul и class
            if main_ul: # если есть ul
                li_lst = main_ul.find_all('li', attrs={'class': 'list-jobs__item'}) # тогда ищем все li которые имет класс list-jobs__item
                for li in li_lst:
                        title = li.find('div', attrs={'class': 'list-jobs__title'})# тайтл с урл
                        href = title.a['href'] # добираемся до  урл
                        cont = li.find('div', attrs={'class': 'list-jobs__description'})# описание
                        content = cont.text
                        company = 'No name'
                        comp = li.find('div', attrs={'class': 'list-jobs__details__info'})
                        if comp:
                            company = comp.text # обращаемся ко всему тексту
                        jobs.append({'title': title.text, 'url': domain + href, # ссылка
                                    'description': content, 'company': company,
                                     'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Table does not exists"})
        else:
            errors.append({'url': url, 'title': "Page is empty"})

    return jobs, errors


if __name__ == '__main__':
    # url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'
    url = 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&primary_keyword=Python'
    jobs, errors = djinni(url)# функция
    h = codecs.open('work.txt', 'w', 'utf-8')# открываем в режиме записи и залдаем кодировку 'utf-8'
    h.write(str(jobs))# записываем весь контент словарем
    h.close()