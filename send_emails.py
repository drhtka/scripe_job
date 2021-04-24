# -*- coding: utf-8 -*-
import os, sys
import django
import datetime

from django.core.mail import EmailMultiAlternatives

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))  # абсолютный путь 8 мин 51 less
sys.path.append(proj)  # добавить в системные переменные путей
os.environ[
    "DJANGO_SETTINGS_MODULE"] = 'scripe_job.settings'  # будет установлена в переменных окружения, указываем название проекта где файл settings.py

django.setup()
from scraping.models import Vacancy, Error, Url

from scripe_job.settings import EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today() # день в которые делаем отправку
subject = f"Рассылка вакансий за {today}"# в заголовке будет понятн оза какое число рассылка
text_content = f"Рассылка вакансий {today}"
from_email = EMAIL_HOST_USER

empty = '<h2>К сожалению на сегодня по Вашим предпочтениям данных нет. </h2>'


User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'language', 'email')# сделали словарь где ключ город и язык программирования
users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['language']), [])
    users_dct[(i['city'], i['language'])].append(i['email'])  # для пары город язык прог, добавляем емаил
if users_dct:  # есть ли хоть кто то кому делать рассылку
    params = {'city_id__in': [],
              'language_id__in': []}  # __in  орм значенре обозначает найти все значения которые принадлежат этой паре

    for pair in users_dct.keys():  # приготовили выборку значений по городу и ЯП из базы данных
        params['city_id__in'].append(pair[0])
        params['language_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()# добавим параметр к полю timestamp=today когда отправлять, т.е. сегодня
    vacancies = {}
    for i in qs:
        vacancies.setdefault((i['city_id'], i['language_id']), [])
        vacancies[(i['city_id'], i['language_id'])].append(i)  # append(i) весб запро который есть. потом выберем необходимые значения
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows: # формируем html с текстом для для отправки всем укзанным
            html += f'<h3"><a href="{ row["url"] }">{ row["title"] }</a></h3>' # title вакансии
            html += f'<p>{row["description"]} </p>'
            html += f'<p>{row["company"]} </p><br><hr>'
        _html = html if html else empty# если html отсутсвует тогд а он равен empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to]
            )
            msg.attach_alternative(_html, "text/html")
            msg.send()

qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():# если ошибки есь, тогда можем отправлять
    error = qs.first()# товы привести к единому экземпляру т.е. на одну дату
    data = error.data.get('errors', [])
    for i in data:# i это словарь всегда
        _html += f'<p"><a href="{ i["url"] }">Error: { i["title"] }</a></p><br>'
        subject = f'ошибки скраинга {today}'
        text_content = 'ошибки скраинга'
        data = error.data.get('user_data')
    if data:
        _html += '<hr>'
        _html += '<h2>Пожелания пользователей </h2>'
        for i in data:
            _html += f'<p">Город: {i["city"]}, Специальность:{i["language"]},  Имейл:{i["email"]}</p><br>'
        subject += f" Пожелания пользователей {today}"
        text_content += "Пожелания пользователей"

qs = Url.objects.all().values('city', 'language')
urls_dct = {(i['city'], i['language']) for i in  qs}
urls_err = ''
for keys in users_dct.keys():
    if keys not in users_dct:# есть лю ключ в словаре с урл
        if keys[0] and keys[1]:  # чтобы н еобрабатывапть пользователей у которрых ничего нет
            urls_err += f'<p"> Для города: {keys[0]} и ЯП: {keys[1]} отсутствуют урлы</p><br>' # поменять эти айдишники {keys[0]} и ЯП: {keys[1]} при помощи выгрузки из базы на названия

if urls_err:
    subject += ' Отсутствующие урлы '
    _html += '<hr>'
    _html += '<h2>Отсутствующие урлы </h2>'
    _html += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
# subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
# text_content = 'This is an important message.'
# html_content = '<p>This is an <strong>important</strong> message.</p>'
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
# msg.attach_alternative(html_content, "text/html")
# msg.send()

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# msg = MIMEMultipart('alternative')
# msg['Subject'] = 'Список вакансий за  {}'.format(today)
# msg['From'] = EMAIL_HOST_USER
# mail = smtplib.SMTP()
# mail.connect(EMAIL_HOST, 25)
# mail.ehlo()
# mail.starttls()
# mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#
# html_m = "<h1>Hello world</h1>"
# part = MIMEText(html_m, 'html')
# msg.attach(part)
# mail.sendmail(EMAIL_HOST_USER, [to], msg.as_string())
# mail.quit()