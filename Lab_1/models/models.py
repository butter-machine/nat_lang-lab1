from django.db import models

from Lab_1.models.querysets import FileModelQuerySet


class FileModel(models.Model):
    file_name = models.CharField(max_length=512)
    file_size = models.PositiveSmallIntegerField()

    objects = FileModelQuerySet.as_manager()

    class Meta:
        unique_together = ('file_size', 'file_name', )

    def __str__(self):
        return self.file_name


class FileToken(models.Model):
    token = models.CharField(max_length=64)
    key_word_coefficient = models.FloatField(null=True)
    count = models.PositiveSmallIntegerField(null=True)
    file = models.ForeignKey(FileModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.token
