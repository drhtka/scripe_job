import requests
import codecs# и меняем сразу кодировку 'utf-8'
from bs4 import BeautifulSoup as BS


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
domain = 'https://www.work.ua'
url = 'https://www.work.ua/ru/jobs-kyiv-python/'
resp = requests.get(url, headers=headers) # делаем запрос представишись брайзером и что то вернет в отвер
jobs = []
errors = []

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



h = codecs.open('work.txt', 'w', 'utf-8')# открываем в режиме записи и залдаем кодировку 'utf-8'
h.write(str(jobs))# записыаем весь контент
h.close