# Generated by Django 2.2.2 on 2019-12-13 15:20

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import image_cropping.fields
import opportunities.models
import opportunities.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('trends', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opportunities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='', max_length=500, verbose_name='Заголовок Возможности')),
                ('imageOld', models.ImageField(default='', upload_to=opportunities.models.Opportunities.user_directory_path, validators=[opportunities.validators.validate_image], verbose_name='Картинка к возможности')),
                ('checkTitle', models.BooleanField(default=True, verbose_name='Заголовок на картинке')),
                ('image', image_cropping.fields.ImageRatioField('imageOld', '390x280', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text='Выберите область для отображения картинки', hide_image_field=False, size_warning=True, verbose_name='Выберите область')),
                ('imageBig', image_cropping.fields.ImageRatioField('imageOld', '900x315', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text='Выберите область для отображения картинки в большом варианте', hide_image_field=False, size_warning=True, verbose_name='Большая картинка')),
                ('address', models.CharField(blank=True, default='', max_length=300, verbose_name='Место проведения')),
                ('map', models.CharField(blank=True, default='', max_length=1501, verbose_name='Ссылка на яндекс-карту')),
                ('time', models.CharField(blank=True, default='', max_length=60, verbose_name='Время проведения')),
                ('dateEnd', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата окончания/проведения')),
                ('dateStart', models.DateField(blank=True, null=True, verbose_name='Дата начала(ОСТАВЬТЕ ПУСТЫМ, ЕСЛИ У ВОЗМОЖНОСТИ НЕТ ПЕРИОДА ПРОВЕДЕНИЯ)')),
                ('date', models.CharField(default='', max_length=100, verbose_name='Строковое представление даты')),
                ('trends', models.ManyToManyField(blank=True, to='trends.Trends', verbose_name='Выберите Направления')),
            ],
            options={
                'ordering': ['-dateEnd'],
                'verbose_name_plural': 'Возможности',
                'verbose_name': 'Возможность',
            },
        ),
        migrations.CreateModel(
            name='OpportunitiesBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topLine', models.BooleanField(default=False, verbose_name='Верхняя линия')),
                ('title', models.CharField(blank=True, default='', max_length=101, verbose_name='Подзаголовок')),
                ('text', ckeditor.fields.RichTextField(blank=True, default='', verbose_name='Текст')),
                ('bottomLine', models.BooleanField(default=False, verbose_name='Нижняя линия')),
                ('customOrder', models.PositiveIntegerField(default=0, verbose_name='Перетащите на нужное место')),
                ('include', models.BooleanField(verbose_name='Блок включен в возможность')),
                ('id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opportunities.Opportunities')),
            ],
            options={
                'ordering': ['customOrder'],
                'verbose_name_plural': 'Блоки возможности',
                'verbose_name': 'Блок возможности',
            },
        ),
        migrations.CreateModel(
            name='OpportunitiesFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, default='', upload_to='opportunities/', validators=[opportunities.validators.validate_file_extension], verbose_name='Картинка или видео')),
                ('ext', models.CharField(blank=True, max_length=5)),
                ('label', models.CharField(blank=True, max_length=150, verbose_name='Подпись к файлу')),
                ('id_fk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='opportunities.OpportunitiesBlock')),
            ],
            options={
                'verbose_name_plural': 'Файл',
                'verbose_name': 'Файл',
            },
        ),
        migrations.AddIndex(
            model_name='opportunitiesblock',
            index=models.Index(fields=['title'], name='opportuniti_title_ffad2f_idx'),
        ),
        migrations.AddIndex(
            model_name='opportunitiesblock',
            index=models.Index(fields=['text'], name='opportuniti_text_b24384_idx'),
        ),
        migrations.AddIndex(
            model_name='opportunities',
            index=models.Index(fields=['title'], name='opportuniti_title_537795_idx'),
        ),
    ]