from django.contrib import admin

from .models import Colum,Articl
class Columadmin(admin.ModelAdmin):
    list_display = ('name','slug','intro','nav_display', 'home_display')

class Articladmin(admin.ModelAdmin):
    list_display = ('title','slug','author','pub_date','update_time')

admin.site.register(Colum,Columadmin)
admin.site.register(Articl,Articladmin)
