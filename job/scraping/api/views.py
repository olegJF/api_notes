from rest_framework.viewsets import ModelViewSet
from scraping.models import City, Specialty, Vacancy
from .serializers import *


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class SpecialtyViewSet(ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

