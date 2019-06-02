from rest_framework.serializers import ModelSerializer
from scraping.models import City, Specialty, Vacancy


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = ('name', 'slug')


class SpecialtySerializer(ModelSerializer):

    class Meta:
        model = Specialty
        fields = ('name', 'slug')


class VacancySerializer(ModelSerializer):

    class Meta:
        model = Vacancy
        fields = '__all__'
