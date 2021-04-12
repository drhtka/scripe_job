import requests
import codecs# и меняем сразу кодировку 'utf-8'
from bs4 import BeautifulSoup as BS


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

def work(url):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    resp = requests.get(url, headers=headers) # делаем запрос представишись брайзером и что то вернет в отвер
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
                                'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': "Table does not exists"})
    else:
        errors.append({'url': url, 'title': "Page is empty"})

    return jobs, errors

def rabota(url):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    # url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    resp = requests.get(url, headers=headers) # делаем запрос представишись брайзером и что то вернет в отвер
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
                                company = p.a.text
                            jobs.append({'title': title.text, 'url': domain + href, 
                                        'description': content, 'company': company})
            else:
                errors.append({'url': url, 'title': "Table does not exists"})
        else:
            errors.append({'url': url, 'title': "Page is empty"})
    else:
        errors.append({'url': url, 'title': "Page do not response"})
    return jobs, errors

def dou(url):
    jobs = []
    errors = []
    # domain = 'https://www.work.ua'
    # url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    resp = requests.get(url, headers=headers) # делаем запрос представишись брайзером и что то вернет в отвер
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
                                'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': "Table does not exists"})
    else:
        errors.append({'url': url, 'title': "Page is empty"})

    return jobs, errors
if __name__ == '__main__':
    url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'
    jobs, errors = dou(url)# функция
    h = codecs.open('work.txt', 'w', 'utf-8')# открываем в режиме записи и залдаем кодировку 'utf-8'
    h.write(str(jobs))# записываем весь контент
    h.close