import os, sys
project_dir = os.path.dirname(os.path.abspath('db_dj.py'))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'find_it.settings'
import django
django.setup()

from django.db import IntegrityError
import datetime
from scraping.utils import *
from scraping.models import *
from subscribers.models import *

def get_all_specialty():
    qs = Subscriber.objects.filter(is_active=True)
    todo_list = {i.city:set() for i in qs}
    for i in qs:
        todo_list[i.city].add(i.specialty)
    return todo_list

def get_urls(todo_list):
    url_list = []
    for city in todo_list:
        for sp in todo_list[city]:
            tmp = {}
            qs = Url.objects.filter(city=city, specialty=sp)
            if qs:
                tmp['city'] = city
                tmp['specialty'] = sp
                for item in qs:
                    tmp[item.site.name] = item.url_address
                url_list.append(tmp)
    return url_list


def scraping_sites():
    todo_list = get_all_specialty()
    url_list = get_urls(todo_list)
    jobs = []
    for url in url_list:
        tmp = {}
        tmp_content = []
        tmp_content.extend(djinni(url['Djinni.co']))
        tmp_content.extend(rabota(url['Rabota.ua']))
        tmp_content.extend(work(url['Work.ua']))
        tmp_content.extend(dou(url['Dou.ua']))
        tmp['city'] = url['city']
        tmp['specialty'] = url['specialty']
        tmp['content'] = tmp_content
        jobs.append(tmp)
    return jobs

def save_to_db():
    all_data = scraping_sites()
    if all_data:
        for data in all_data:
            city = data['city']
            specialty = data['specialty']
            jobs = data['content'] 
            for job in jobs:
                vacancy = Vacancy(city=city, specialty=specialty, url=job['href'],
                                title=job['title'], description=job['descript'], company=job['company'])
                try:
                    vacancy.save()
                except IntegrityError:
                    pass
    return True

print(save_to_db())