from django.contrib import admin

from account.models import Profil


class ProfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


admin.site.register(Profil, ProfilAdmin)