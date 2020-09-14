from django.db import models

from Lab_1.models.querysets import FileModelQuerySet


class FileModel(models.Model):
    file_name = models.CharField(max_length=512)
    file_size = models.PositiveSmallIntegerField()

    tokens = models.ManyToManyField('Token')

    objects = FileModelQuerySet.as_manager()

    class Meta:
        unique_together = ('file_size', 'file_name', )


class Token(models.Model):
    token = models.CharField(max_length=64)
