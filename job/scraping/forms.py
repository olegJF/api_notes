from django import forms
from scraping.models import Specialty, City

class FindVacancyForm(forms.Form):
    city = forms.ModelChoiceField( label='Город', queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    specialty = forms.ModelChoiceField( label='Специальность', queryset=Specialty.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
