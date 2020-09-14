from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from Lab_1.forms import SearchForm
from Lab_1.services import DocumentSearchService, DatabaseService, SearchTokenizer, IndexService


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {'form': SearchForm()}


def search_form_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            tokenizer = SearchTokenizer()
            database_service = DatabaseService()
            indexer = IndexService(tokenizer, database_service)
            search_service = DocumentSearchService(tokenizer, indexer)

            request.session['texts'] = search_service.search(request.POST['search'])
            return HttpResponseRedirect(reverse('result'))
    else:
        form = SearchForm()

    return render(request, 'index.html', {'form': form})


class ResultView(TemplateView):
    template_name = 'result.html'

    def get_context_data(self, **kwargs):
        return {
            'texts': self.request.session['texts'],
            'search_page_url': '/'
        }
