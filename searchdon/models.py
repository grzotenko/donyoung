from django.db import models
from main.models import Main
# Create your models here.
class SettingsSearch(models.Model):
    RS_CHOICES = (
        (True, "Да"),
        (False, "Нет"),
    )
    id_fk = models.ForeignKey(Main, on_delete=models.CASCADE)
    factorTitle = models.IntegerField(verbose_name="Множитель заголовка", blank=True)
    factorPreview = models.IntegerField(verbose_name="Множитель превью", blank=True)
    factorText = models.IntegerField(verbose_name="Множитель текста", blank=True)
    factorPage = models.IntegerField(verbose_name="Множитель исходной страницы", blank=True)
    filterGTE = models.DecimalField(verbose_name="Минимальная граница попадания в поисковый запрос", max_digits=5, decimal_places=2, blank=True)
    rank_similarity = models.BooleanField(choices=RS_CHOICES, verbose_name="Поиск, ориентированный на точное совпадение", default=False)
    class Meta:
        verbose_name = "Настройки поиска"
        verbose_name_plural = "Настройки поиска"
    def __str__(self):
        return "Выбранные"