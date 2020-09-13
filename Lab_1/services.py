import os

from django.conf import settings
import nltk
from django.core.files.base import ContentFile
from nltk.corpus import stopwords

from Lab_1.models.models import FileModel

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
    def process_file(file):
        if FileModel.objects.by_file(file) is None:
            new_file = FileModel(file_name=file.name, file_size=file.size)
            new_file.save()

            return new_file

        return None


class DocumentSearchService:
    def __init__(self):
        self.search_tokenizer = SearchTokenizer()
        self.database_service = DatabaseService()

    def search(self, search_string):
        search_result = []
        for filename in os.listdir(BASE_DIR):
            with open(os.path.join(BASE_DIR, filename), 'r') as f:
                content_file = ContentFile(f.read(), name=f.name)
                f.seek(0)
                file_tokens = self.search_tokenizer.tokenize(content_file.read())
                search_tokens = self.search_tokenizer.tokenize(search_string)

                if file_tokens.intersection(search_tokens):
                    new_file_model = self.database_service.process_file(content_file)

                    if new_file_model is not None:
                        file_name = os.path.basename(new_file_model.file_name)
                        content = f.read()
                    else:
                        file_path = FileModel.objects.by_file(content_file).file_name
                        with open(file_path, 'r') as storage_file:
                            file_name = os.path.basename(file_path)
                            content = storage_file.read()

                    search_result.append({'file_name': file_name, 'content': content})

        return search_result
