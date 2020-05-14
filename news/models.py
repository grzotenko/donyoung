from django.db import models
from django.utils import timezone
from .validators import validate_file_extension, validate_image
from django.utils.safestring import mark_safe       #for imagePreView
from django.db.models import Max
from trends.models import Trends
from image_cropping import ImageRatioField, ImageCropField
from django.contrib.postgres.indexes import GinIndex
from ckeditor.fields import RichTextField
# Create your models here.
class News(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.app_label,instance.id, filename)
    title = models.TextField(max_length=400, verbose_name="Заголовок Новости", blank=False, default='')
    titlePreview = models.TextField(max_length=500, verbose_name="Превью Новости", blank=True, default='')
    date = models.DateTimeField(default=timezone.now, blank=False, verbose_name="Дата и Время")
    imageOld = models.ImageField(validators=[validate_image], blank=False, default='', verbose_name="Картинка к новости", upload_to=user_directory_path)
    image = ImageRatioField('imageOld', '300x300', help_text="Выберите область для отображения картинки в маленьком варианте", verbose_name="Маленькая картинка")
    imageBig = ImageRatioField('imageOld', '900x315', help_text="Выберите область для отображения картинки в большом варианте", verbose_name="Большая картинка")
    trends = models.ManyToManyField(Trends, verbose_name="Выберите Направления", blank=True)
    main = models.BooleanField(default=False, verbose_name="Главная новость")
    important = models.BooleanField(default=False, verbose_name="Важная новость")
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
            super(News, self).save(*args, **kwargs)
            self.imageOld = saved_image
        return super(News, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.app_label,self.id)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors = True)
        return super(News, self).delete(*args, **kwargs)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-date"]
        indexes = (
            models.Index(fields=['titlePreview']),
            models.Index(fields=['title']),
        )

class NewsBlock(models.Model):
    id_fk = models.ForeignKey(News, on_delete=models.CASCADE)
    topLine = models.BooleanField(blank=False, default=False, verbose_name="Верхняя линия")
    title = models.CharField(blank=True,  default="", max_length=101, verbose_name="Подзаголовок")
    text = RichTextField(blank=True,  default="", verbose_name="Текст")
    bottomLine = models.BooleanField(blank=False, default=False, verbose_name="Нижняя линия")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")
    include = models.BooleanField(blank=False, verbose_name="Блок включен в новость")
    def __str__(self):
        if self.title is "" or self.title is None:
            return str(self.customOrder)
        else:
            return self.title

    class Meta(object):
        verbose_name = "Блок новости"
        verbose_name_plural = "Блоки новости"
        ordering = ['customOrder']
        indexes = (
            models.Index(fields=['title']),
            models.Index(fields=['text']),
        )
class NewsFile(models.Model):
    id_fk = models.OneToOneField(NewsBlock, on_delete=models.CASCADE)
    file = models.FileField(blank=True, default='', validators=[validate_file_extension], verbose_name="Картинка или видео", upload_to='news/')
    ext = models.CharField(max_length=5, blank=True)
    label = models.CharField(max_length=150, verbose_name="Подпись к файлу", blank=True)
    def save(self, *args, **kwargs):
        ext = self.file.name.split('.')[-1]
        img_extensions = ['jpg', 'png', 'jpeg']
        video_extensions = ['avi', 'mpeg4', 'mp4']
        if ext.lower() in img_extensions:
                self.ext = 'img'
        elif ext.lower() in video_extensions:
                self.ext = 'video'
        return super(NewsFile, self).save(*args, **kwargs)
    def imagePreView(self):
        if self.ext == "img":
            return mark_safe('<img src="/media/%s" height="50" />' % (self.file))
        # return mark_safe('<img src="/media/%s" height="150" />' % (self.image))
    imagePreView.short_description = 'Предпросмотр картинки'
    def __str__(self):
        return "Картинка или видео"
    class Meta(object):
        verbose_name = "Файл"
        verbose_name_plural = "Файл"
