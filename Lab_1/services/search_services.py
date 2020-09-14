import os

import nltk
from nltk.corpus import stopwords

from Lab_1.models.models import FileModel, FileToken
from Lab_1.settings import KEY_WORDS_COEFFICIENT

nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')


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

    def tokenize(self, text):
        tokens = self.tokenizer.tokenize(text)
        tokens = self._clean_tokens(tokens)
        tokens = self._stem_tokens(tokens)

        return tokens


class DocumentSearchService:
    def __init__(self, tokenizer):
        self.search_tokenizer = tokenizer

    def search(self, search_string):
        search_tokens = self.search_tokenizer.tokenize(search_string)
        search_queryset = FileModel.objects.filter(
            tokens__in=FileToken.objects.filter(token__in=search_tokens),
            token_key_word_coefficient__gte=KEY_WORDS_COEFFICIENT
        )

        search_results = []
        for file_model in search_queryset:
            with open(file_model.file_name, 'r') as storage_file:
                content = storage_file.read()
            file_name = os.path.basename(file_model.file_name)

            search_results.append({'file_name': file_name, 'content': content})

        return search_results
