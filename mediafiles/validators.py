# -*- coding: utf-8 -*-
def validate_file_extension(value):
    from django.core.exceptions import ValidationError
    ext = value.name.split('.')[-1]
    valid_extensions = ['jpg', 'png', 'jpeg', 'mp4', 'avi', 'mpeg4']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Не поддерживаемое расширение файла')
def validate_documents(value):
    from django.core.exceptions import ValidationError
    ext = value.name.split('.')[-1]
    valid_extensions = ['doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt', 'pdf', 'mp4', 'jpg', ]
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Не поддерживаемое расширение файла')

def validate_image(value):
    from django.core.exceptions import ValidationError
    ext = value.name.split('.')[-1]
    valid_extensions = ['jpg', 'png', 'jpeg', 'svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Не поддерживаемое расширение файла')