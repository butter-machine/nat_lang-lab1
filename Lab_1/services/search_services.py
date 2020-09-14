import os

import nltk
from django.db.models import Q, F
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
        search_result = FileModel.objects.filter(
            filetoken__in=FileToken.objects.filter(token__in=search_tokens),
            filetoken__key_word_coefficient__gte=KEY_WORDS_COEFFICIENT
        ).values('pk', 'file_name')

        for result in search_result:
            with open(result['file_name'], 'r') as storage_file:
                content = storage_file.read()
            result['content'] = content
            result['tokens'] = sorted(
                list(
                    FileToken.objects.filter(file_id=result['pk']).values(
                        'token',
                        'key_word_coefficient',
                        'count'
                    )
                ),
                key=lambda x: x['key_word_coefficient'],
                reverse=True
            )

        return list(search_result)
