# Generated by Django 2.2.2 on 2019-12-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default='', max_length=254, verbose_name='Электронная почта подписчика')),
            ],
            options={
                'verbose_name_plural': 'Подписчики',
                'verbose_name': 'Подписчик',
            },
        ),
    ]