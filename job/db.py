import psycopg2
import logging
import datetime
import os
import json
from scraping.utils import *
from elasticsearch import Elasticsearch

today = datetime.date.today()
UTILS_FUNC = [(djinni, 'Djinni.co'), (work, 'Work.ua'),
            (rabota, 'Rabota.ua'), (dou, 'Dou.ua')]
ten_days_ago = datetime.date.today() - datetime.timedelta(10)
dir = os.path.dirname(os.path.abspath('db.py'))
path = ''.join([dir, '\\find_it\\secret.py'])
if os.path.exists(path):
    from find_it.secret import DB_PASSWORD, DB_HOST, DB_NAME, DB_USER
else:
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    ES_PASSWORD = os.environ.get('ES_PASSWORD')
    ES_HOST = os.environ.get('ES_HOST')
    ES_USER = os.environ.get('ES_USER')
 
try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, 
                                password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, specialty_id FROM subscribers_subscriber 
                    WHERE is_active=%s;""", (True,))
    cities_qs = cur.fetchall()
    # print(cities_qs)
    todo_list = {i[0]:set() for i in cities_qs}
    for i in cities_qs:
        todo_list[i[0]].add(i[1])
    # print(todo_list)
    cur.execute("""SELECT * FROM scraping_site; """)
    sites_qs = cur.fetchall()
    sites = {i[0]: i[1] for i in sites_qs}
    # print(sites)
    url_list = []
    for city in todo_list:
        for sp in todo_list[city]:
            
            tmp = {}
            cur.execute("""SELECT site_id, url_address FROM scraping_url 
                    WHERE city_id=%s AND specialty_id=%s;""", (city, sp))
            qs = cur.fetchall()
            # print(qs)
            if qs:
                # cur.execute(""" SELECT legal_words FROM scraping_specialty 
                #         WHERE id=%s;""", (str(sp)))
                # sp_qs = cur.fetchone()
                # legal_words = sp_qs[0] if sp_qs[0] else None
                tmp['city'] = city
                tmp['specialty'] = sp
                # tmp['legal_words'] = legal_words
                for item in qs:
                    site_id = item[0]
                    tmp[sites[site_id]] = item[1]
                url_list.append(tmp)
    # print(url_list)
    all_data = []
    errors = []
    if url_list:
        for url in url_list:
            tmp = {}
            tmp_content = []
            for (func, key) in UTILS_FUNC:
                # print(key, url['legal_words'])
                j, e = func(url.get(key, None), None) # url['legal_words'])
                tmp_content.extend(j)
                errors.extend(e)
            tmp['city'] = url['city']
            tmp['specialty'] = url['specialty']
            tmp['content'] = tmp_content
            all_data.append(tmp)
    # print('get data')
    if all_data:
        for data in all_data:
            city = data['city']
            specialty = data['specialty']
            jobs = data['content'] 
            for job in jobs:
                cur.execute("""SELECT * FROM scraping_vacancy 
                                WHERE url=%s; """, (job['href'], ))
                qs = cur.fetchone()
                if not qs:
                    cur.execute("""INSERT INTO scraping_vacancy 
                                    (city_id, specialty_id, title,
                                    url, description, company, timestamp) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s); """, 
                                 (city, specialty, job['title'],job['href'], 
                                 job['descript'], job['company'], today ))

    if errors:
        cur.execute("""SELECT data FROM scraping_error 
                        WHERE timestamp=%s; """, (today, ))
        err_qs = cur.fetchone()
        if err_qs:
            data = err_qs[0]
            data['errors'].extend(errors)
            cur.execute("""UPDATE scraping_error SET data=%s 
                            WHERE timestamp=%s;""", (json.dumps(data), today,))
        else:
            data = {}
            data['errors'] = errors
            cur.execute("""INSERT INTO scraping_error (data, timestamp) 
                            VALUES (%s, %s); """, (json.dumps(data), today ))
                                 
    

    # cur.execute("""SELECT url, title, description, company, timestamp, 
    #                 city_id, specialty_id FROM  scraping_vacancy 
    #                 WHERE timestamp<=%s;""", (ten_days_ago,))
    # qs = cur.fetchall()
    # if qs:
    #     vacancies = []
    #     cur.execute(""" SELECT * FROM scraping_city;""")
    #     cities_qs = cur.fetchall()
    #     cities = {i[0]: i[1] for i in cities_qs}
    #     cur.execute(""" SELECT * FROM scraping_specialty;""")
    #     sp_qs = cur.fetchall()
    #     sp = {i[0]: i[1] for i in sp_qs}
    #     try:
    #         es = Elasticsearch(ES_HOST, http_auth=(ES_USER, ES_PASSWORD))
    #     except:
    #         pass
    #     else:
    #         for q in qs:
    #             data = {'url': q[0], 'title': q[1], 
    #                             'description': q[2], 
    #                             'company': q[3],
    #                             'timestamp': q[4],
    #                             'city': cities[q[5]],
    #                             'specialty': sp[q[6]]}
    #             try:
    #                 res = es.index(index='jobs', doc_type='live', body=data)
    #             except:
    #                 pass
                    
    cur.execute("""DELETE FROM  scraping_vacancy WHERE timestamp<=%s;""", 
                   (ten_days_ago,))

    conn.commit()
    cur.close()
    conn.close()