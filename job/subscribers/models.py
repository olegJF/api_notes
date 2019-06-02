import uuid
from django.db import models
from scraping.models import City, Specialty


class Subscriber(models.Model):
    email = models.CharField(max_length=100, unique=True, verbose_name='E-mail')
    city = models.ForeignKey(City, verbose_name='Город' , on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, verbose_name='Специальность' , on_delete=models.CASCADE)
    password = models.CharField(max_length=100,  verbose_name='Пароль')
    token = models.UUIDField(default=uuid.uuid4, editable=False) 
    is_active = models.BooleanField(default=True, verbose_name='Получать рассылку?')

    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
