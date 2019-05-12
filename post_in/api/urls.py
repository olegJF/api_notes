from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import *

urlpatterns = [
    path('notes/', notes_list),
    path('notes/<int:pk>/', notes_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)