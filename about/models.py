from django.db import models
from .validators import validate_file_extension, validate_image
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField

# Create your models here.
class About(models.Model):
    work_time = RichTextField(default='', blank=False, verbose_name="Режим работы")
    text = RichTextField(default='', blank=False, verbose_name="Информация")
    email = models.CharField(default='', blank=False, verbose_name="Электронная почта", max_length=100)
    phone = models.CharField(default='', blank=False, verbose_name="Телефон", max_length=20)
    address = models.CharField(blank=True, default="", max_length=301, verbose_name="Адрес")
    map = models.CharField(blank=True, default="", max_length=1501, verbose_name="Ссылка на Яндекс-карту")

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"

    def __str__(self):
        return "РЕДАКТИРОВАТЬ 'О НАС'"
class AboutBlock(models.Model):
    id_fk = models.ForeignKey(About, on_delete=models.CASCADE)
    title = models.CharField(default='', blank=False, verbose_name="Название отдела", max_length=200)
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False,
                                              verbose_name="Перетащите на нужное место")
    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"
        ordering = ["customOrder"]

class AboutBlockPeople(models.Model):
    id_fk = models.ForeignKey(AboutBlock, on_delete=models.CASCADE)
    name = models.CharField(default='', blank=False, verbose_name="ФИО", max_length=100)
    image = models.ImageField(validators=[validate_image], blank=False, default='', verbose_name="Картинка", upload_to='about/')
    position = models.CharField(default='', blank=False, verbose_name="Должность", max_length=100)
    email = models.CharField(default='', blank=False, verbose_name="Электронная почта", max_length=100)
    phone = models.CharField(default='', blank=False, verbose_name="Номер телефона", max_length=20)
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False,
                                              verbose_name="Перетащите на нужное место")
    def __str__(self):
        return self.name

    def imagePreView(self):
        return mark_safe('<img src="/media/%s" height="50" />' % (self.image))
    imagePreView.short_description = 'Предпросмотр картинки'

    class Meta(object):
        verbose_name = "Работник"
        verbose_name_plural = "Работники"
        ordering = ["customOrder"]