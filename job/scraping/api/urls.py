from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('cities', CityViewSet)
router.register('sp', SpecialtyViewSet)
router.register('vacancy', VacancyViewSet)
urlpatterns = router.urls