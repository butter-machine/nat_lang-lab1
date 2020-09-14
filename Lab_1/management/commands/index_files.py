from django.core.management.base import BaseCommand

from Lab_1.services.index_services import IndexService, DatabaseService
from Lab_1.services.search_services import SearchTokenizer


class Command(BaseCommand):
    def handle(self, *args, **options):
        IndexService(SearchTokenizer(), DatabaseService()).index_files()
