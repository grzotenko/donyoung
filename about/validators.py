# -*- coding: utf-8 -*-
def validate_file_extension(value):
    from django.core.exceptions import ValidationError
    ext = value.name.split('.')[-1]
    valid_extensions = ['jpg', 'png', 'jpeg', 'webm', 'mp4', 'avi']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Не поддерживаемое расширение файла')

def validate_image(value):
    from django.core.exceptions import ValidationError
    ext = value.name.split('.')[-1]
    valid_extensions = ['jpg', 'png', 'jpeg', 'svg', 'webm']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Не поддерживаемое расширение файла')