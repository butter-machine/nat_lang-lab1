from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from Lab_1.forms import SearchForm
from Lab_1.services import DocumentSearchService


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {'form': SearchForm()}


def search_form_view(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_service = DocumentSearchService()

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
