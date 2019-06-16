import datetime
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from scraping.models import City, Specialty, Vacancy
from .serializers import *

period = datetime.date.today() - datetime.timedelta(1)


class DateFilterBackend(filters.BaseFilterBackend):
    
    def filter_queryset(self, request, queryset, view):
        city_slug = request.query_params.get('city', None)
        sp_slug = request.query_params.get('sp', None)
        return queryset.filter( 
            city__slug=city_slug,
            specialty__slug=sp_slug,
            timestamp__gte=period)

class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SpecialtyViewSet(ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class VacancyViewSet(ModelViewSet):
    """
    ?city=kyiv&sp=python
    """
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, DateFilterBackend)
    filterset_fields = ('city__slug', 'specialty__slug')

    # def get_queryset(self):
    #     city_slug = self.request.query_params.get('city', None)
    #     sp_slug = self.request.query_params.get('sp', None)
    #     qs = None
    #     if city_slug and sp_slug:
    #         qs = Vacancy.objects.filter(
    #             city__slug=city_slug, 
    #             specialty__slug=sp_slug, timestamp__gte=period)
    #     self.queryset = qs
    #     return self.queryset

    # def get_queryset(self):
    #     city_slug = self.request.query_params.get('city', None)
    #     sp_slug = self.request.query_params.get('sp', None)
    #     qs = None
    #     if city_slug and sp_slug:
    #         city = City.objects.filter(slug=city_slug).first()
    #         sp = Specialty.objects.filter(slug=sp_slug).first()
    #         if city and sp:
    #             qs = Vacancy.objects.filter(city=city, specialty=sp, timestamp__gte=period)
    #     self.queryset = qs
    #     return self.queryset
    #  resp['result'][-1][''message]['chat']['id']
