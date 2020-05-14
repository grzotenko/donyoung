# Generated by Django 2.2.2 on 2020-01-31 08:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flagmans', '0004_auto_20191213_1840'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flagmans',
            options={'ordering': ['dateStart', 'dateEnd'], 'verbose_name': 'Флагман', 'verbose_name_plural': 'Флагманы'},
        ),
        migrations.AlterField(
            model_name='flagmans',
            name='dateEnd',
            field=models.DateField(blank=True, null=True, verbose_name='Дата окончания/проведения(ОСТАВЬТЕ ПУСТЫМ, ЕСЛИ У ФЛАГМАНА НЕТ ПЕРИОДА ПРОВЕДЕНИЯ)'),
        ),
        migrations.AlterField(
            model_name='flagmans',
            name='dateStart',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата начала'),
        ),
    ]
