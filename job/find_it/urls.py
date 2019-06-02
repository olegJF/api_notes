from django.urls import include, path
from django.contrib import admin
from scraping.views import *
from subscribers.views import *
import os

TOKEN = os.environ.get('BOT_TOKEN')

urlpatterns = [
    path('adminka/', admin.site.urls),
    path('list/', vacancy_list, name='list'),
    path('login/', login_subscriber, name='login'),
    path('update/', update_subscriber, name='update'),
    path('create/', SubscriberCreate.as_view(), name='create'),
    path('contact/', contact_admin, name='contact'),
    path('delete/', delete_subscriber, name='delete'),
    path('', index, name='index'),
    path('api/v1/', include('scraping.api.urls')),
]
