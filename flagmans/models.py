from django.db import models
from .validators import *
from django.utils import timezone
from image_cropping import ImageRatioField
# Create your models here.
class Flagmans(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.app_label,instance.id, filename)

    title = models.CharField(max_length=150, verbose_name="Название флагмана", blank=False, default='')
    imageOld = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка", upload_to=user_directory_path)
    image = ImageRatioField('imageOld', '320x300', help_text="Выберите область для отображения картинки", verbose_name="Отображение картинки")
    address = models.CharField(blank=True, default="", max_length=301, verbose_name="Место проведения")
    url = models.CharField(blank=True, default="", max_length=201, verbose_name="Ссылка")
    map = models.CharField(blank=True, default="", max_length=1501, verbose_name="Ссылка на яндекс-карту")
    dateStart = models.DateField(default=timezone.now, blank=False, verbose_name="Дата начала")
    dateEnd = models.DateField(blank=True, verbose_name="Дата окончания/проведения(ОСТАВЬТЕ ПУСТЫМ, ЕСЛИ У ФЛАГМАНА НЕТ ПЕРИОДА ПРОВЕДЕНИЯ)", null=True)
    date = models.CharField(max_length=100, verbose_name="Строковое представление даты", default="", blank=False)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if self.id:
            import os, glob
            path = './media/{0}/{1}/*.*'.format(self._meta.app_label,self.id)
            pathOld = '.{0}*.*'.format(self.imageOld.url)
            filesOld = glob.glob(pathOld)
            filesOld.append("." + self.imageOld.url)
            for file in glob.glob(path):
                if file not in filesOld:
                    os.remove(file)
        else:
            saved_image = self.imageOld
            self.imageOld = None
            super(Flagmans, self).save(*args, **kwargs)
            self.imageOld = saved_image
        return super(Flagmans, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.app_label,self.id)
        if os.path.exists(path):
            shutil.rmtree(path)
        return super(Flagmans, self).delete(*args, **kwargs)
    class Meta(object):
        verbose_name = "Флагман"
        verbose_name_plural = "Флагманы"
        ordering = ['dateStart', 'dateEnd']
        indexes = (
            models.Index(fields=['title']),
            models.Index(fields=['address']),
        )