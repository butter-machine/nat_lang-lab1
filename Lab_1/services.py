import os

from django.conf import settings
import nltk
from django.core.files.base import ContentFile
from nltk.corpus import stopwords

from Lab_1.models.models import FileModel, Token

nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

BASE_DIR = settings.SEARCH_FILES_DIR


class SearchTokenizer:
    def __init__(self):
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
        self.stemmer = nltk.PorterStemmer()

    @staticmethod
    def _clean_tokens(tokens):
        stop_words = set(stopwords.words('english'))
        return [token.lower() for token in tokens if token not in stop_words]

    def _stem_tokens(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]

    def tokenize(self, text: str):
        tokens = self.tokenizer.tokenize(text)
        tokens = self._clean_tokens(tokens)
        tokens = self._stem_tokens(tokens)

        return set(tokens)


class DatabaseService:
    @staticmethod
    def add_file_if_not_exists(file, file_tokens):
        if FileModel.objects.by_file(file) is None:
            new_file = FileModel(file_name=file.name, file_size=file.size)
            new_file.save()

            token_models = [Token.objects.get_or_create(token=token)[0].id for token in file_tokens]
            new_file.tokens.set(token_models)

            return new_file

        return None


class IndexService:
    def __init__(self, tokenizer, database_service):
        self.search_tokenizer = tokenizer
        self.database_service = database_service

    def index_files(self):
        for filename in os.listdir(BASE_DIR):
            with open(os.path.join(BASE_DIR, filename), 'r') as f:
                content_file = ContentFile(f.read(), name=f.name)
                f.seek(0)

            file_tokens = self.search_tokenizer.tokenize(content_file.read())
            self.database_service.add_file_if_not_exists(content_file, file_tokens)


class DocumentSearchService:
    def __init__(self, tokenizer, indexer):
        self.search_tokenizer = tokenizer
        self.indexer = indexer

    def search(self, search_string):
        search_tokens = self.search_tokenizer.tokenize(search_string)

        self.indexer.index_files()

        search_queryset = FileModel.objects.filter(tokens__token__in=search_tokens)
        search_results = []

        for file_model in search_queryset:
            with open(file_model.file_name, 'r') as storage_file:
                content = storage_file.read()
            file_name = os.path.basename(file_model.file_name)

            search_results.append({'file_name': file_name, 'content': content})

        return search_results
