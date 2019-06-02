from django.shortcuts import render
from django.http import Http404
from django.db import IntegrityError
import datetime
from scraping.utils import *
from scraping.models import *
from scraping.forms import FindVacancyForm



def list_v(request):
    today = datetime.date.today()
    city = City.objects.get(name='Львов')
    specialty = Specialty.objects.get(name='Python')
    qs = Vacancy.objects.filter(city=city.id, specialty=specialty.id, timestamp=today)
    if qs:
        return render(request, 'scraping/list.html', {'jobs': qs})
    return render(request, 'scraping/list.html')



def home(request):
    city = City.objects.get(name='Киев')
    specialty = Specialty.objects.get(name='Python')
    url_qs = Url.objects.filter(city=city, specialty=specialty)
    site = Site.objects.all()
    url_w = url_qs.get(site=site.get(name='Work.ua')).url_address
    url_dj = url_qs.get(site=site.get(name='Djinni.co')).url_address
    url_r = url_qs.get(site=site.get(name='Rabota.ua')).url_address
    url_dou = url_qs.get(site=site.get(name='Dou.ua')).url_address
    jobs = []
    jobs.extend(djinni(url_dj))
    jobs.extend(rabota(url_r))
    jobs.extend(work(url_w))
    jobs.extend(dou(url_dou))
    
    # v = Vacancy.objects.filter(city=city.id, specialty=specialty.id).values('url')
    # url_list = [i['url'] for i in v]
    for job in jobs:
        vacancy = Vacancy(city=city, specialty=specialty, url=job['href'],
                                title=job['title'], description=job['descript'], company=job['company'])
        try:
            vacancy.save()
        except IntegrityError:
            pass

    return render(request, 'scraping/list.html', {'jobs': jobs})