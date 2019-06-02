import requests
from bs4 import BeautifulSoup as BS
import codecs
import time
import datetime
import random

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]
def djinni(base_url, legal_words):
    jobs = []
    urls = []
    errors = []
    if base_url:
        session = requests.Session()
        domain = 'https://djinni.co'
        urls.append(base_url)
        urls.append(base_url+'&page=2')

        for url in urls:
            time.sleep(2)
            nmb = random.randint(0, 2)
            req = session.get(url, headers=headers[nmb])
            if req.status_code == 200:
                bsObj = BS(req.content, "html.parser")
                li_list = bsObj.find_all('li', attrs={'class': 'list-jobs__item'})
                if li_list:
                    for li in li_list:
                        div = li.find('div', attrs={'class': 'list-jobs__title'})
                        title = div.a.text
                        href = div.a['href']
                        short = 'No description'
                        # company = "No name"
                        descr = li.find('div', attrs={'class': 'list-jobs__description'})
                        if descr:
                            short = descr.p.text
                        jobs.append({'href': domain + href,
                                    'title': title, 
                                    'descript': short,
                                    'company': "No name"})
                else:
                    errors.append({'href': url,
                                'title': 'The page is empty'})
            else:
                errors.append({'href': url,
                                'title': 'Page do not respose'})
    return jobs, errors

def rabota(base_url, legal_words):
    jobs = []
    urls = []
    errors = []
    if base_url:
        session = requests.Session()
        domain = 'https://rabota.ua'
        yesterday = datetime.date.today()-datetime.timedelta(1)
        one_day_ago = yesterday.strftime('%d.%m.%Y')
        base_url = base_url + one_day_ago
        urls.append(base_url)

        nmb = random.randint(0, 2)
        req = session.get(base_url, headers=headers[nmb])
        if req.status_code == 200:
            bsObj = BS(req.content, "html.parser")
            pagination = bsObj.find('dl', 
                    attrs={'id': 
                    'ctl00_content_vacancyList_gridList_ctl23_pagerInnerTable' 
                        })# ctl00_content_VacancyListAws_gridList_ctl23_pagerInnerTable
            if pagination:
                pages = pagination.find_all('a', attrs={'class': 'f-always-blue'})
                for page in pages:
                    urls.append(domain + page['href'])
        else:
            errors.append({'href': base_url,
                                'title': 'Page do not respose'})
        # print(urls)
        # legal_words = legal_words.split(' ') if legal_words else None
        for url in urls:
            time.sleep(2)
            nmb = random.randint(0, 2)
            req = session.get(url, headers=headers[nmb])
            if req.status_code == 200:
                bsObj = BS(req.content, "html.parser")
                new_jobs_found = not(bsObj.find('div', 
                                attrs={'class': 'f-vacancylist-newnotfound'}))
                if new_jobs_found:
                    table = bsObj.find('table', 
                            attrs={'id': 'ctl00_content_vacancyList_gridList'}) 
                                        # ctl00_content_VacancyListAws_gridList
                    if table:
                        tr_list = bsObj.find_all('tr', attrs={'id': True})
                        for tr in tr_list:
                            h3 = tr.find('h3', 
                                    attrs={'class': 'f-vacancylist-vacancytitle'})
                            title = h3.a.text
                            href = h3.a['href']
                            short = 'No description'
                            company = "No name"
                            logo = tr.find('p', 
                                        attrs={'class': 'f-vacancylist-companyname'})
                            if logo:
                                try:
                                    company = logo.text
                                except:
                                    pass
                            p = tr.find('p', 
                                        attrs={'class': 'f-vacancylist-shortdescr'})
                            if p:
                                short = p.text
                            # if legal_words:
                            #     '''Если слова из legal_words есть в заглавии или в описании, 
                            #         тогда добавляем эту вакансию в список.'''
                            #     words_in_title = any((w in title.lower() for w in legal_words))
                            #     words_in_descript = any((w in short.lower() for w in legal_words))
                            #     if any( (words_in_title, words_in_descript)):
                            #         jobs.append({'href': domain + href,
                            #                     'title': title, 
                            #                     'descript': short,
                            #                     'company': company})
                            # else:
                            jobs.append({'href': domain + href,
                                        'title': title, 
                                        'descript': short,
                                        'company': company})

                        
                else:
                    errors.append({'href': url,
                                'title': 'The page is empty'})
            else:
                errors.append({'href': url,
                                'title': 'Page do not respose'})
    return jobs, errors


def work(base_url, legal_words):
    jobs = []
    urls = []
    errors = []
    if base_url:
        session = requests.Session()
        domain = 'https://www.work.ua'
        urls.append(base_url)
        nmb = random.randint(0, 2)
        req = session.get(base_url, headers=headers[nmb])
        if req.status_code == 200:
            bsObj = BS(req.content, "html.parser")
            pagination = bsObj.find('ul', attrs={'class': 'pagination'})
            if pagination:
                pages = pagination.find_all('li', attrs={'class': False})
                for page in pages:
                    urls.append(domain + page.a['href'])
        else:
            errors.append({'href': base_url,
                                'title': 'Page do not respose'})
        for url in urls:
            time.sleep(2)
            nmb = random.randint(0, 2)
            req = session.get(url, headers=headers[nmb])
            if req.status_code == 200:
                bsObj = BS(req.content, "html.parser")
                div_list = bsObj.find_all('div', attrs={'class': 'job-link'})
                if div_list:
                    for div in div_list:
                        title = div.find('h2')
                        href = title.a['href']
                        short = div.p.text
                        company = "No name"
                        logo = div.find('img')
                        if logo:
                            company = logo['alt']
                        jobs.append({'href': domain + href,
                                    'title': title.text, 
                                    'descript': short,
                                    'company': company})
                else:
                    errors.append({'href': url,
                                'title': 'The page is empty'})
            else:
                errors.append({'href': url,
                                'title': 'Page do not respose'})

    return jobs, errors


def dou(base_url, legal_words):
    
    jobs = []
    urls = []
    errors = []
    if base_url:
        urls.append(base_url)
        session = requests.Session()

        for url in urls:
            time.sleep(2)
            nmb = random.randint(0, 2)
            req = session.get(url, headers=headers[nmb])
            if req.status_code == 200:
                bsObj = BS(req.content, "html.parser")
                div = bsObj.find('div', attrs={'id': 'vacancyListId'})
                if div:
                    li_list = bsObj.find_all('li', attrs={'class': 'l-vacancy'})
                    for li in li_list:
                        a = li.find('a', attrs={'class': 'vt'})
                        title = a.text
                        href = a['href']
                        short = 'No description'
                        company = "No name"
                        a_company = li.find('a', attrs={'class': 'company'})
                        if a_company:
                            company = a_company.text
                        descr = li.find('div', attrs={'class': 'sh-info'})
                        if descr:
                            short = descr.text
                        jobs.append({'href': href,
                                    'title': title, 
                                    'descript': short,
                                    'company': company})
                else:
                    errors.append({'href': url,
                                'title': 'The page is empty'})
            else:
                errors.append({'href': url,
                                'title': 'Page do not respose'})    
    return jobs, errors