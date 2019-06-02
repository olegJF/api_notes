from django import forms
from subscribers.models import Subscriber
from scraping.models import Specialty, City

class SubscriberModelForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={"class": 'form-control'}))
    city = forms.ModelChoiceField( label='Город', queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    specialty = forms.ModelChoiceField( label='Специальность', queryset=Specialty.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(label='''Я согласен получать рассылку 
                                    по вакансиям, на указанный мной e-mail''', 
                                    required=True, widget=forms.CheckboxInput(
                                    attrs={'class': 'form-check-input', 
                                    'checked': "checked"}))
    
    class Meta:
        model = Subscriber
        fields = ('email', 'city', 'specialty', 'password', 'is_active')
        

class LogInForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            qs = Subscriber.objects.filter(email=email).first()
            if qs == None:
                raise forms.ValidationError("""Пользователя с таким и-мэйлом не существует """)
            elif password != qs.password:
                raise forms.ValidationError("""Неверный пароль! """)

        return email


class SubscriberHiddenEmailForm(forms.ModelForm):
    city = forms.ModelChoiceField( label='Город', queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    specialty = forms.ModelChoiceField( label='Специальность', queryset=Specialty.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.HiddenInput())
    is_active = forms.BooleanField(label='Получать рассылку?', required=False, widget=forms.CheckboxInput() )

    class Meta:
        model = Subscriber
        fields = ('email', 'city', 'specialty', 'password', 'is_active')

class ContactForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={"class": 'form-control'}))
    city = forms.CharField( label='Город', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialty = forms.CharField( label='Специальность', required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    

class TokenForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    token = forms.CharField(widget=forms.HiddenInput())