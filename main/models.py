from django.db import models
from .validators import *
from django.utils.safestring import mark_safe       #for imagePreView
from image_cropping import ImageRatioField

# Create your models here.
class Main(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}/{3}'.format(instance._meta.app_label,instance._meta.model_name,instance.id, filename)
    banner = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Баннер",upload_to=user_directory_path)
    logo = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Лого",upload_to=user_directory_path)
    copyright = models.TextField(max_length=300, verbose_name="Копирайт", blank=False, default='')

    def __str__(self):
        return "ИЗМЕНИТЬ ГЛАВНУЮ СТРАНИЦУ"

    class Meta:
        verbose_name = "Главная"
        verbose_name_plural = "Главные"

class HeaderMenu(models.Model):
    id_fk = models.ForeignKey(Main, on_delete=models.CASCADE, related_name='menu')
    title = models.CharField(blank=False,  default="", max_length=30, verbose_name="Название элемента меню")
    path = models.CharField(blank=False,  default="", max_length=101, verbose_name="Путь")

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = "Меню"
        verbose_name_plural = "Меню"


class HeaderOrganizers(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}/{3}'.format(instance._meta.app_label,instance._meta.model_name,instance.id, filename)
    id_fk = models.ForeignKey(Main, on_delete=models.CASCADE, related_name='organizers')
    url = models.CharField(blank=False,  default="", max_length=101, verbose_name="Ссылка")
    image = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка", upload_to=user_directory_path)
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")

    def __str__(self):
        return str(self.id)

    class Meta():
        verbose_name = "Организатор"
        verbose_name_plural = "Организаторы"
        ordering = ['customOrder']

class SocialNet(models.Model):
    id_fk = models.ForeignKey(Main, on_delete=models.CASCADE,related_name='socialnet')
    vk = models.CharField(blank=False, default="", max_length=101, verbose_name="Вконтакте")
    instagram = models.CharField(blank=False, default="", max_length=101, verbose_name="Instagram")
    youtube = models.CharField(blank=False, default="", max_length=101, verbose_name="YouTube")
    facebook = models.CharField(blank=False, default="", max_length=101, verbose_name="Facebook")

    def __str__(self):
        return "ВКонтакте, YouTube, Facebook, Instagram"

    class Meta(object):
        verbose_name = "Социальные сети"
        verbose_name_plural = "Социальные сети"



class FooterPartners(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}/{3}'.format(instance._meta.app_label,instance._meta.model_name,instance.id, filename)
    id_fk = models.ForeignKey(Main, on_delete=models.CASCADE, related_name='partners')
    url = models.CharField(blank=False, default="", max_length=101, verbose_name="Ссылка")
    imageOld = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка",
                              upload_to=user_directory_path)
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")
    image = ImageRatioField('imageOld', '50x50', help_text="Выберите область для отображения картинки", verbose_name="Отображение картинки")

    def __str__(self):
        return self.url

    class Meta(object):
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ['customOrder']
    def save(self, *args, **kwargs):
        if self.id:
            import os, glob
            path = './media/{0}/{1}/{2}/*.*'.format(self._meta.app_label,self._meta.model_name,self.id)
            pathOld = '.{0}*.*'.format(self.imageOld.url)
            filesOld = glob.glob(pathOld)
            filesOld.append("." + self.imageOld.url)
            for file in glob.glob(path):
                if file not in filesOld:
                    os.remove(file)
        return super(FooterPartners, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}/{2}'.format(self._meta.app_label,self._meta.model_name,self.id)
        if os.path.exists(path):
            shutil.rmtree(path)
        return super(FooterPartners, self).delete(*args, **kwargs)
class FooterContacts(models.Model):
    id_fk = models.ForeignKey(Main, on_delete=models.CASCADE)
    title = models.CharField(blank=False, default="", max_length=51, verbose_name="Заголовок")
    phone = models.CharField(blank=False, default="", max_length=20, verbose_name="Телефон")
    email = models.CharField(blank=False, default="", max_length=101, verbose_name="Почта")
    address = models.CharField(blank=False, default="", max_length=301, verbose_name="Адрес")
    map = models.CharField(blank=True, default="", max_length=1501, verbose_name="Ссылка на яндекс-карту")

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"