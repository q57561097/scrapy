from django.contrib import admin

from .models import Zlzp,Zwxx
class Zlzpadmin(admin.ModelAdmin):
    list_display = ('gsmc','gsjj','nav_display', 'home_display')

class Zwxxadmin(admin.ModelAdmin):
    list_display = ('zwmc','zwyx','gzdd','gsmz','pub_date','update_time')

admin.site.register(Zlzp,Zlzpadmin)
admin.site.register(Zwxx,Zwxxadmin)
