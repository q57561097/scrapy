from django.shortcuts import render
from  django.shortcuts import redirect
from .models import Zwxx,Zlzp
def Zpxx(request):
    zwlbs=Zwxx.objects.all()
    return render(request,'zlzp/zpxx.html',{'zwlbs':zwlbs})
def Zwyq(request,pk):
        zwxxi = Zwxx.objects.get(pk=pk)
        gsxx=Zlzp.objects.get(gsmc=zwxxi.gsmz)


        return render(request, 'zlzp/zwyq.html', {'zwxxi': zwxxi,'gsxx':gsxx})