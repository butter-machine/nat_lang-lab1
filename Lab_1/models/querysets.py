from django.db.models import QuerySet


class FileModelQuerySet(QuerySet):
    def by_file(self, file):
        try:
            return self.get(
                file_name=file.name,
                file_size=file.size
            )
        except self.model.DoesNotExist:
            return None
