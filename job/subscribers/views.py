from django.shortcuts import render, redirect, get_object_or_404
from .forms import (SubscriberModelForm, LogInForm, 
                    SubscriberHiddenEmailForm, ContactForm, TokenForm)
from django.views.generic.edit import FormView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings
from .models import Subscriber

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


ADMIN_EMAIL = settings.ADMIN_EMAIL
MAILGUN_KEY = settings.MAILGUN_KEY
API = settings.API
MAIL_SERVER = settings.MAIL_SERVER
PASSWORD_AWARD = settings.PASSWORD_AWARD
USER_AWARD = settings.USER_AWARD
FROM_EMAIL = settings.FROM_EMAIL


class SubscriberCreate(CreateView):
    model = Subscriber
    form_class = SubscriberModelForm
    template_name = 'subscribers/create.html'
    success_url = reverse_lazy('create')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.success(request, 'Данные успешно сохранены.')
            return self.form_valid(form)
        else:
            messages.error(request, 'Проверьте правильность заполнения формы')
            return self.form_invalid(form)

def login_subscriber(request):
    if request.method == "GET":
        form = LogInForm
        return render(request, 'subscribers/login.html', {'form': form})
    elif request.method == "POST":
        form = LogInForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            request.session['email'] = data['email']
            return redirect('update')
        return render(request, 'subscribers/login.html', {'form': form})
        

def update_subscriber(request):
    if request.method == 'GET' and request.session.get('email', False):
        email = request.session.get('email')
        qs = Subscriber.objects.filter(email=email).first()
        token_form = TokenForm(initial={'email': qs.email, 'token': qs.token})
        form = SubscriberHiddenEmailForm(initial={'email': qs.email, 
                                                    'city': qs.city, 
                                                    'specialty': qs.specialty, 
                                                    'password': qs.password, 
                                                    'is_active': qs.is_active})
        return render(request, 'subscribers/update.html', 
                                                {'form': form, 
                                                'token_form': token_form})
    elif request.method == 'POST':
        email = request.session.get('email')
        user = get_object_or_404(Subscriber, email=email)
        form = SubscriberHiddenEmailForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно сохранены.')
            del request.session['email']
            return redirect('index')
        messages.error(request, 'Проверьте правильность заполнения формы')
        return render(request, 'subscribers/update.html', {'form': form})
    else:
        return redirect('login')


def delete_subscriber(request):
    if request.method == 'POST':
        email = request.session.get('email')
        user = get_object_or_404(Subscriber, email=email)
        form = TokenForm(request.POST or None)
        if form.is_valid():
            form_email = form.cleaned_data['email']
            form_token = form.cleaned_data['token']
            token = str(user.token)
            # assert False 
            if email == form_email and token == form_token:
                user.delete()
                messages.success(request, 'Данные успешно удалены.')
                del request.session['email']
                return redirect('index')
        messages.error(request, 'Проверьте правильность заполнения формы')
        return render(request, 'subscribers/update.html')
    else:
        return redirect('login')



def contact_admin(request):
    if request.method =='POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            city = form.cleaned_data['city']
            specialty = form.cleaned_data['specialty']
            from_email = form.cleaned_data['email']
            content = 'Прошу добавить в поиск : город - {}'.format(city)
            content += ', специальность - {}'.format(specialty)
            content += 'Запрос от пользователя  {}'.format(from_email)
            # Subject = 'Запрос на добавление в БД'
            msg = MIMEMultipart()
            msg['Subject'] = 'Запрос на добавление в БД'
            msg['From'] = '<{email}>'.format(email=FROM_EMAIL)
            msg['To'] = ADMIN_EMAIL
            mail = smtplib.SMTP()
            mail.connect(MAIL_SERVER, 25)
            mail.ehlo()
            mail.starttls()
            mail.login(USER_AWARD, PASSWORD_AWARD)
            email = [ADMIN_EMAIL]
            msg.attach(MIMEText(content))
            mail.sendmail(FROM_EMAIL, email, msg.as_string())
            # requests.post(API,  auth=("api", MAILGUN_KEY), data={"from": from_email, "to": ADMIN_EMAIL,
            #                     "subject":Subject , "text": content})
            messages.success(request, 'Ваше письмо отправленно')
            mail.quit()
            return redirect('index')
        return render(request, 'subscribers/contact.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'subscribers/contact.html', {'form': form})