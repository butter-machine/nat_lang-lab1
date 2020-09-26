import math
import os

from django.core.files.base import ContentFile
from tqdm import tqdm

from Lab_1 import settings
from Lab_1.models.models import FileModel, FileToken


BASE_DIR = settings.SEARCH_FILES_DIR


class DatabaseService:
    @staticmethod
    def get_files_count():
        return FileModel.objects.all().count()

    @staticmethod
    def get_files_with_token_count(token):
        return FileModel.objects.filter(filetoken__token=token).count()

    @staticmethod
    def add_file(file):
        new_file = FileModel(file_name=file.name, file_size=file.size)
        new_file.save()

        return new_file

    @staticmethod
    def add_tokens(file_model, tokens):
        token_models = []
        for token in tokens:
            token_model, _ = FileToken.objects.get_or_create(token=token)
            token_model.count = tokens.count(token)
            token_model.file = file_model
            token_model.save()
            token_models.append(token_model)

        return token_models

    @staticmethod
    def update_token_model_wit_key_word_coefficient(token_model, key_word_coefficient):
        token_model.key_word_coefficient = key_word_coefficient
        token_model.save()

        return token_model


class IndexService:
    def __init__(self, tokenizer, database_service):
        self.search_tokenizer = tokenizer
        self.database_service = database_service

    @staticmethod
    def _open_file(file_path):
        with open(os.path.join(BASE_DIR, file_path), 'r') as f:
            content_file = ContentFile(f.read(), name=f.name)
            f.seek(0)

        return content_file

    def _calculate_tokens_key_word_coefficients(self, token, files_count, tokens_entry_count):
        inverse_frequency = math.log(files_count / self.database_service.get_files_with_token_count(token))
        return inverse_frequency * tokens_entry_count

    def index_files(self):
        for filename in os.listdir(BASE_DIR):
            content_file = self._open_file(filename)
            if FileModel.objects.by_file(content_file) is not None:
                continue

            self.database_service.add_file(content_file)

        file_models_queryset = FileModel.objects.all()
        for file_model in tqdm(file_models_queryset):
            content_file = self._open_file(file_model.file_name)
            file_model = FileModel.objects.by_file(content_file)
            if file_model.processed:
                continue

            file_tokens = self.search_tokenizer.tokenize(content_file.read())
            token_models = self.database_service.add_tokens(file_model, file_tokens)

            for token_model in token_models:
                coefficient = self._calculate_tokens_key_word_coefficients(
                    token_model,
                    file_models_queryset.count(),
                    file_tokens.count(token_model.token)
                )

                self.database_service.update_token_model_wit_key_word_coefficient(token_model, coefficient)

            file_model.processed = True
