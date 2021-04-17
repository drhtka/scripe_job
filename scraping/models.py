# -*- coding: utf-8 -*-
import jsonfield
from django.db import models
from scraping.utils import from_cyrillic_to_eng


def default_urls():
    return {"work": "", "rabota": "", "dou": "", "djinni": ""} #55 less готовим словарь

class City(models.Model):
    class Meta:
        verbose_name = 'Город название'
        verbose_name_plural = 'Города название'

    name = models.CharField(max_length=50, verbose_name='Название населенного пункта', unique=True)
    slug = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)

class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Язык программирования',
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город', related_name='vacancies')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()

    class Meta:
        verbose_name = 'Ошибки'
        verbose_name_plural = 'Ошибки'
        ordering = ['-timestamp']
    def __str__(self):
        return str(self.timestamp)

class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE,
                             verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 verbose_name='Язык программирования')
    url_data = jsonfield.JSONField(default=default_urls)#т.е. мы подготовили словарь

    def __str__(self):
        # return "{}, {}".format(self.title, self.user)
        return "Город: {} и ЯП: {}".format(self.city, self.language)
    class Meta:
        verbose_name = 'URL адреса'
        verbose_name_plural = 'URL адреса'
        unique_together = ("city", "language") # т.е для города киев и специальности пайтон не может быть больше чем одна строка