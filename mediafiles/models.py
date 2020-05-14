from django.db import models
from .validators import *
from django.utils.safestring import mark_safe       #for imagePreView
from image_cropping import ImageRatioField
# Create your models here.
class MediaFiles(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name="Название блока", blank=False, default='')
    urlPhotos = models.CharField(blank=False, default="", max_length=201, verbose_name="Ссылка на альбомы вк")
    urlVideos = models.CharField(blank=False, default="", max_length=201, verbose_name="Ссылка на ютуб-канал")
    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name="Медиа"
        verbose_name_plural="Медиа"
class MediaPhotos(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.app_label,instance.id, filename)

    id_fk = models.ForeignKey(MediaFiles, on_delete=models.CASCADE)
    url = models.CharField(blank=False, default="", max_length=201, verbose_name="Ссылка")
    imageOld = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка",
                              upload_to=user_directory_path)
    image = ImageRatioField('imageOld', '280x140', help_text="Выберите область для отображения картинки", verbose_name="Отображение картинки")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")
    title = models.CharField(blank=False, default="", max_length=201, verbose_name="Название")
    def __str__(self):
        return str(self.id)


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
        return super(MediaPhotos, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.app_label,self.id)
        if os.path.exists(path):
            shutil.rmtree(path)
        return super(MediaPhotos, self).delete(*args, **kwargs)


    class Meta(object):
        verbose_name = "Фотоальбом"
        verbose_name_plural = "Фотоальбомы"
        ordering = ['customOrder']


class MediaVideos(models.Model):
    id_fk = models.ForeignKey(MediaFiles, on_delete=models.CASCADE)
    url = models.CharField(blank=False, default="", max_length=201, verbose_name="Ссылка")
    title = models.CharField(blank=False, default="", max_length=201, verbose_name="Название")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False,
                                              verbose_name="Перетащите на нужное место")

    def __str__(self):
        return str(self.id)

    class Meta(object):
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ['customOrder']
