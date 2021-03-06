# Generated by Django 2.2.2 on 2019-12-13 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettingsSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factorTitle', models.IntegerField(blank=True, verbose_name='Множитель заголовка')),
                ('factorPreview', models.IntegerField(blank=True, verbose_name='Множитель превью')),
                ('factorText', models.IntegerField(blank=True, verbose_name='Множитель текста')),
                ('factorPage', models.IntegerField(blank=True, verbose_name='Множитель исходной страницы')),
                ('filterGTE', models.DecimalField(blank=True, decimal_places=2, max_digits=5, verbose_name='Минимальная граница попадания в поисковый запрос')),
                ('rank_similarity', models.BooleanField(choices=[(True, 'Да'), (False, 'Нет')], default=False, verbose_name='Поиск, ориентированный на точное совпадение')),
                ('id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Main')),
            ],
            options={
                'verbose_name_plural': 'Настройки поиска',
                'verbose_name': 'Настройки поиска',
            },
        ),
    ]
