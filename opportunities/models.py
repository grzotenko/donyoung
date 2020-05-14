from django.db import models
from trends.models import Trends
from django.utils import timezone
from image_cropping import ImageRatioField
from .validators import validate_file_extension, validate_image
from django.utils.safestring import mark_safe       #for imagePreView
from ckeditor.fields import RichTextField

# Create your models here.
class Opportunities(models.Model):
    def user_directory_path(instance, filename):
        return '{0}/{1}/{2}'.format(instance._meta.app_label,instance.id, filename)
    title = models.TextField(max_length=500, verbose_name="Заголовок Возможности", blank=False, default='')
    imageOld = models.ImageField(validators=[validate_image], blank=False, default='', verbose_name="Картинка к возможности",
                              upload_to=user_directory_path)
    checkTitle = models.BooleanField(default=True, verbose_name="Заголовок на картинке")
    image = ImageRatioField('imageOld', '390x280', help_text="Выберите область для отображения картинки", verbose_name="Выберите область")
    imageBig = ImageRatioField('imageOld', '900x315', help_text="Выберите область для отображения картинки в большом варианте", verbose_name="Большая картинка")

    address = models.CharField(default='', verbose_name="Место проведения", blank=True, max_length=300)
    map = models.CharField(blank=True, default="", max_length=1501, verbose_name="Ссылка на яндекс-карту")
    time = models.CharField(default='', verbose_name="Время проведения", blank=True,max_length=60 )
    dateStart = models.DateField(default=timezone.now, blank=True, null=True, verbose_name="Дата начала")
    dateEnd = models.DateField(blank=True,verbose_name="Дата окончания/проведения(ОСТАВЬТЕ ПУСТЫМ, ЕСЛИ У ВОЗМОЖНОСТИ НЕТ ПЕРИОДА ПРОВЕДЕНИЯ)",null=True)
    date = models.CharField(max_length=100, verbose_name="Строковое представление даты", default="", blank=False)
    trends = models.ManyToManyField(Trends, verbose_name="Выберите Направления",blank=True)
    main = models.BooleanField(default=False, verbose_name="Отображение на главной странице")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Возможность"
        verbose_name_plural = "Возможности"
        ordering = ['dateStart', 'dateEnd']
        indexes = (
            models.Index(fields=['title']),
        )
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
            super(Opportunities, self).save(*args, **kwargs)
            self.imageOld = saved_image
        return super(Opportunities, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        import os, shutil
        path = './media/{0}/{1}'.format(self._meta.app_label,self.id)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors = True)
        return super(Opportunities, self).delete(*args, **kwargs)


class OpportunitiesBlock(models.Model):
    id_fk = models.ForeignKey(Opportunities, on_delete=models.CASCADE)
    topLine = models.BooleanField(blank=False, default=False, verbose_name="Верхняя линия")
    title = models.CharField(blank=True, default="", max_length=101, verbose_name="Подзаголовок")
    text = RichTextField(blank=True, default="", verbose_name="Текст")
    bottomLine = models.BooleanField(blank=False, default=False, verbose_name="Нижняя линия")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False,
                                              verbose_name="Перетащите на нужное место")
    include = models.BooleanField(blank=False, verbose_name="Блок включен в возможность")

    def __str__(self):
        if self.title is "" or self.title is None:
            return str(self.customOrder)
        else:
            return self.title

    class Meta(object):
        verbose_name = "Блок возможности"
        verbose_name_plural = "Блоки возможности"
        ordering = ['customOrder']
        indexes = (
            models.Index(fields=['title']),
            models.Index(fields=['text']),
        )

class OpportunitiesFile(models.Model):
    id_fk = models.OneToOneField(OpportunitiesBlock, on_delete=models.CASCADE)
    file = models.FileField(blank=True, default='', validators=[validate_file_extension], verbose_name="Картинка или видео", upload_to='opportunities/')
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
        return super(OpportunitiesFile, self).save(*args, **kwargs)
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