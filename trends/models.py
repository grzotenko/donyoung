from django.db import models
from .validators import *
from django.utils.safestring import mark_safe       #for imagePreView
from ckeditor.fields import RichTextField

# Create your models here.
class Trends(models.Model):
    title = models.CharField(max_length=300, unique=True, verbose_name="Название направления", blank=False, default='')
    text = RichTextField(verbose_name="Текст", blank=False, default='')
    imageInactive = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка неактивная",
                              upload_to='trends/')
    imageActive = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка при наведении",
                              upload_to='trends/')
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False,
                                              verbose_name="Перетащите на нужное место")
    def __str__(self):
        return self.title

    def imagePreView(self):
        return mark_safe('<img src="/media/%s" height="50" />' % (self.imageInactive))
    imagePreView.short_description = 'Предпросмотр картинки'

    class Meta(object):
        verbose_name="Направление"
        verbose_name_plural="Направления"
        ordering = ['customOrder']
        indexes = (
            models.Index(fields=['title']),
            models.Index(fields=['text']),
        )

class TrendsContacts(models.Model):
    id_fk = models.ForeignKey(Trends, on_delete=models.CASCADE)
    name = models.CharField(blank=False, default="", max_length=150, verbose_name="Имя")
    position = models.CharField(blank=True, default="", max_length=201, verbose_name="Должность")
    image = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка",
                              upload_to='trends/')
    phone = models.CharField(blank=True, default="", max_length=20, verbose_name="Телефон")
    email = models.CharField(blank=True, default="", max_length=101, verbose_name="Почта")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")

    def __str__(self):
        return self.name

    def imagePreView(self):
        return mark_safe('<img src="/media/%s" height="50" />' % (self.image))
    imagePreView.short_description = 'Предпросмотр картинки'

    class Meta(object):
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ['customOrder']
        indexes = (
            models.Index(fields=['name']),
            models.Index(fields=['position']),
        )

class TrendsPartners(models.Model):
    id_fk = models.ForeignKey(Trends, on_delete=models.CASCADE)
    title = models.CharField(blank=False, default="", max_length=250, verbose_name="Партнер")
    image = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка",
                              upload_to='trends/')
    url = models.CharField(blank=True, default="", max_length=1001, verbose_name="Ссылка на сайт")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ['customOrder']

    def imagePreView(self):
        return mark_safe('<img src="/media/%s" height="50" />' % (self.image))
    imagePreView.short_description = 'Предпросмотр картинки'


class TrendsDocuments(models.Model):
    id_fk = models.ForeignKey(Trends, on_delete=models.CASCADE)
    title = models.CharField(blank=False, default="", max_length=300, verbose_name="Заголовок")
    file = models.FileField(validators=[validate_documents], blank=True, default='', verbose_name="Файл",
                              upload_to='trends/')
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")

    def __str__(self):
        return str(self.id)

    class Meta(object):
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['customOrder']

class TrendsHrefs(models.Model):
    id_fk = models.ForeignKey(Trends, on_delete=models.CASCADE)
    title = models.CharField(blank=False, default="", max_length=1500, verbose_name="Название")
    url = models.CharField(blank=False, default="", max_length=1500, verbose_name="Ссылка")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")

    def __str__(self):
        return str(self.title)

    class Meta(object):
        verbose_name = "Иная ссылка"
        verbose_name_plural = "Иные ссылки"
        ordering = ['customOrder']