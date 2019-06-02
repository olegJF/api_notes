from django.contrib import admin

from .models import Subscriber

class SubscriberAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Subscriber
    list_display = ( 'email', 'city', 'specialty', 'is_active')
    list_editable = ['is_active']

admin.site.register(Subscriber, SubscriberAdmin)
