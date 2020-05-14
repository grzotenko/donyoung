from django.db import models

# Create your models here.
class Subs(models.Model):
    email = models.EmailField(blank=False, verbose_name="Электронная почта подписчика", default='')
    def __str__(self):
        return self.email
    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"