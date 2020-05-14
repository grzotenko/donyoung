from django.db import models
from .validators import validate_file_extension, validate_image
from django.utils.safestring import mark_safe       #for imagePreView
from ckeditor.fields import RichTextField

# Create your models here.
class DistrictMain(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название", blank=False, default='')
    # youngUsers = models.CharField(max_length=100, verbose_name="Молодых пользователей в регионе", blank=True, default='')
    # municipalAreas = models.IntegerField(blank=True, default=43, verbose_name="Муниципальных районов")
    # urbanAreas = models.IntegerField(blank=True, default=17, verbose_name="Городских округов")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Территория(Главная Страница)"
        verbose_name_plural = "Территории(Главная Страница)"

class District(models.Model):
    id_fk = models.ForeignKey(DistrictMain, on_delete=models.CASCADE)
    title = models.CharField(blank=False,  default="", max_length=201, verbose_name="Название территории")
    image = models.ImageField(validators=[validate_image], blank=False, default='', verbose_name="Карта территории", upload_to='districts/')
    isCity = models.BooleanField(blank=False, default=False, verbose_name="Город")
    isMainCity = models.BooleanField(blank=False, default=False, verbose_name="Главный город территорий")
    phone = models.CharField(blank=True, default="", max_length=20, verbose_name="Телефон")
    email = models.CharField(blank=True, default="", max_length=101, verbose_name="Почта")
    address = models.CharField(blank=True, default="", max_length=301, verbose_name="Адрес")
    map = models.CharField(blank=True, default="", max_length=1501, verbose_name="Ссылка на яндекс-карту")
    url = models.CharField(blank=True, default="", max_length=201, verbose_name="Ссылка на сайт")
    vk = models.CharField(blank=True, default="", max_length=101, verbose_name="Вконтакте")
    instagram = models.CharField(blank=True, default="", max_length=101, verbose_name="Instagram")
    facebook = models.CharField(blank=True, default="", max_length=101, verbose_name="Facebook")
    countYouth = models.CharField(max_length=100, verbose_name="Молодых пользователей", blank=True, default='')
    percentageYouth = models.CharField(max_length=100, verbose_name="Процент молодежи от числа жителей региона",
                                       blank=True, default='')

    def __str__(self):
        return self.title
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if District.objects.filter(isMainCity = True).count() > 0 and self.isMainCity is False:
            self.isMainCity = False
        return super(District, self).save()
    class Meta(object):
        verbose_name = "Территория"
        verbose_name_plural = "Территории"
        ordering = ["-isMainCity","-isCity", "title"]
        indexes = (
            models.Index(fields=['title']),
        )
class Department(models.Model):
    id_fk = models.ForeignKey(District, on_delete=models.CASCADE)
    title = models.CharField(blank=False, default="", max_length=801, verbose_name="Название отдела/сектора")
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False,
                                              verbose_name="Перетащите на нужное место")
    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = "Отдел/Сектор"
        verbose_name_plural = "Отдел/Сектор"
        ordering = ['customOrder']
        indexes = (
                    models.Index(fields=['title']),
                )

class DistrictContacts(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отдел/сектор")
    id_fk = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(blank=False, default="", max_length=301, verbose_name="Имя")
    position = models.CharField(blank=True, default="", max_length=501, verbose_name="Должность")
    image = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Фото",
                              upload_to='districts/')
    phone = models.CharField(blank=True, default="", max_length=300, verbose_name="Телефон")
    email = models.CharField(blank=True, default="", max_length=301, verbose_name="Почта")
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

class Agency(models.Model):
    id_fk = models.OneToOneField(District, on_delete=models.CASCADE)
    title = models.CharField(blank=False, default="", max_length=201, verbose_name="Название органа")
    text = RichTextField(blank=True, default="", max_length=201, verbose_name="Описание")
    image = models.ImageField(validators=[validate_image], blank=True, default='', verbose_name="Картинка",
                              upload_to='districts/')
    customOrder = models.PositiveIntegerField(default=0, blank=False, null=False, verbose_name="Перетащите на нужное место")

    def __str__(self):
        return self.title

    def imagePreView(self):
        return mark_safe('<img src="/media/%s" height="50" />' % (self.image))
    imagePreView.short_description = 'Предпросмотр картинки'

    class Meta(object):
        verbose_name = "Орган"
        verbose_name_plural = "Органы"
        ordering = ['customOrder']
        indexes = (
            models.Index(fields=['title']),
            models.Index(fields=['text']),
        )