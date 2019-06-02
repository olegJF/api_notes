import psycopg2
import logging
import datetime
import os
import requests
import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

today = datetime.date.today()
yesterday = today - datetime.timedelta(1)
dir = os.path.dirname(os.path.abspath('db.py'))
path = ''.join([dir, '\\find_it\\secret.py'])
if os.path.exists(path):
    from find_it.secret import (DB_PASSWORD, DB_HOST, DB_NAME, DB_USER, 
                                MAILGUN_KEY, API, ADMIN_EMAIL, MAIL_SERVER, 
                                PASSWORD_AWARD, USER_AWARD, FROM_EMAIL)
else:
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    MAILGUN_KEY = os.environ.get('MAILGUN_KEY')
    API = os.environ.get('API')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    PASSWORD_AWARD = os.environ.get('PASSWORD_AWARD')
    USER_AWARD = os.environ.get('USER_AWARD')
    FROM_EMAIL = os.environ.get('FROM_EMAIL')
    
# FROM_EMAIL = 'noreply@jobfinderapp.heroku.com'
# SUBJECT = 'Недостающие урлы {}'.format(today)
msg = MIMEMultipart('alternative')
msg['From'] = 'jobfinderapp.heroku.com <{email}>'.format(email=FROM_EMAIL)
msg['To'] = ADMIN_EMAIL
email = [ADMIN_EMAIL]

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute(""" SELECT city_id, specialty_id FROM subscribers_subscriber WHERE is_active=%s;""", (True,))
    qs = cur.fetchall()
    cur.execute(""" SELECT * FROM scraping_city;""")
    cities_qs = cur.fetchall()
    cities = {i[0]: i[1] for i in cities_qs}
    cur.execute(""" SELECT * FROM scraping_specialty;""")
    sp_qs = cur.fetchall()
    sp = {i[0]: i[1] for i in sp_qs}
    mis_urls = []
    cnt = 'На дату {}  отсутствуют урлы для следующих пар:'.format(today)
    mail = smtplib.SMTP()
    mail.connect(MAIL_SERVER, 25)
    mail.ehlo()
    mail.starttls()
    mail.login(USER_AWARD, PASSWORD_AWARD)
    for pair in qs:
        cur.execute("""SELECT * FROM scraping_url  WHERE city_id=%s 
                    AND specialty_id=%s;""", (pair[0], pair[1]))
        qs = cur.fetchall()
        if not qs:
            mis_urls.append((cities[pair[0]], sp[pair[1]]))
    if mis_urls:
        for p in mis_urls:
            cnt += 'город -{}, специальность - {}'.format(p[0], p[1])
        msg['Subject'] = 'Недостающие урлы {}'.format(today)
        
        part = MIMEText(cnt, 'plain')
        msg.attach(part)
        mail.sendmail(FROM_EMAIL, email, msg.as_string())
        time.sleep(2)

    cur.execute("""SELECT data FROM scraping_error 
                                WHERE timestamp=%s; """, (yesterday, ))
    err_qs = cur.fetchone()
    if err_qs:
        msg['Subject'] = 'Ошибки скрапинга по состоянию на {}'.format(yesterday)
        data = err_qs[0]['errors']
        cnt = 'На дату {}  обнаруженны следующие ошибки скрапинга:'.format(yesterday)
        for err in data:
            cnt += 'для url -{}, причина - {}\n'.format(err['href'], err['title'])
            
        part = MIMEText(cnt, 'plain')
        msg.attach(part)
        mail.sendmail(FROM_EMAIL, email, msg.as_string())


    conn.commit()
    cur.close()
    conn.close()
    mail.quit()