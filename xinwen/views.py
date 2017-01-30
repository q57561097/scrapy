#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from .models import Articl,Colum
from django.shortcuts import redirect


def index(request):
    home_display_columns = Colum.objects.filter(home_display=True)
    nav_display_columns = Colum.objects.filter(nav_display=True)

    return render(request, 'index.html', {
        'home_display_columns': home_display_columns,
        'nav_display_columns': nav_display_columns,
    })

def col(request, colum):
    column = Colum.objects.get(slug=colum)
    return render(request, 'xinwen/column.html', {'column': column})


def art(request, pk,articl):
    article = Articl.objects.get(pk=pk)
    if articl != article.slug:
        return redirect(article, permanent=True)
    return render(request, 'xinwen/article.html', {'article': article})