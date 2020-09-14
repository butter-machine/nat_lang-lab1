from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(label='Search words', max_length=100)
