#coding:utf-8
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from cStringIO import StringIO
from .ymm import create_validata_code
from django.views.decorators.cache import cache_page
from itsdangerous import URLSafeTimedSerializer as utsr
from blogs.models import UserProfile
import base64
import re
from django.conf import settings as django_settings
from django.core.mail import send_mail

class Token():
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodestring(b'security_key')
    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)
token_confirm = Token(django_settings.SECRET_KEY)
class RegistForm(forms.Form):

    username=forms.CharField(label='用户名',widget=forms.TextInput(attrs={}))
    password=forms.CharField(label='密码',widget=forms.PasswordInput(attrs={}),)
    email=forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={}))
    phone=forms.CharField(label='电话')
    yzm = forms.CharField(label='验证码',widget=forms.TextInput(attrs={}))
class UserForm(forms.Form):
    username=forms.CharField(label='用户名',error_messages={'required':'用户名不能为空'})

    password=forms.CharField(label='密码',error_messages={'required':'密码不能为空'},widget=forms.PasswordInput())
    yzm=forms.CharField(label='验证码')

class ChangeForm(forms.Form):
    username=forms.CharField(label='用户名')
    oldpassword=forms.CharField(label='原密码',widget=forms.PasswordInput())
    newpassword=forms.CharField(label='新密码',widget=forms.PasswordInput())



def CheckCod(request):
    f = StringIO()
    validate_code = create_validata_code()
    img = validate_code[0]
    img.save(f, "GIF")

    # 将验证码保存到session
    request.session["CheckCode"] = validate_code[1]

    return HttpResponse(f.getvalue())
def regist(request):
    if request.method =='POST':
        uf=RegistForm(request.POST)
        session_code = request.session["CheckCode"]
        tt=session_code.lower()
        if uf.is_valid():
            username=uf.cleaned_data['username']
            password=uf.cleaned_data['password']
            email=uf.cleaned_data['email']
            yzm=uf.cleaned_data['yzm']
            phone=uf.cleaned_data['phone']
            gg = yzm.strip().lower()
            user=User.objects.filter(username=username)
            if user:
                info ='用户已存在'
            elif gg==tt:
                info='请登录到注册邮箱中验证用户，有效期为1个小时'
                user = User.objects.create_user(username=username,

                email = email,

                password = password)
                user.is_active = False
                user.save()

                profile= UserProfile(user=user,phone = phone)


                profile.save()

                token = token_confirm.generate_validate_token(username)
                message ="\n".join([u'{0},欢迎加入我的博客'.format(username), u'请访问该链接，完成用户验证:',
                                 '/'.join([ 'http://localhost:8000/activate/%s'% token])])
                send_mail('注册用户验证信息', message, '13052586986@163.com', [email], fail_silently=False)
            else:
                info='验证码错误'
            return render(request, 'news/regist.html', {'uf': uf, 'info': info})
    else:
        uf=RegistForm()
    return render(request,'news/regist.html',{'uf':uf,})
def login(request):
    if request.method=='POST':
        uf=UserForm(request.POST)

        session_code = request.session["CheckCode"]
        tt=session_code.lower()

        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            yzm=uf.cleaned_data['yzm']
            gg = yzm.strip().lower()
            user = User.objects.filter(username=username)

            if user:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    if tt == gg:
                        auth.login(request, user)
                        return HttpResponseRedirect("/admin/")
                    else:

                        info = '验证码错误'

                else:
                    info='密码错误'
            elif len(user)==0:
                info='用户名不存在'
            return render(request, 'news/login.html', {'uf': uf,'info':info})

    else:
            uf=UserForm()
    return render(request,'news/login.html', {'uf': uf})


def changepass(request):
    if request.method == 'POST':
        uf = ChangeForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            oldpassword = uf.cleaned_data['oldpassword']
            newpassword = uf.cleaned_data['newpassword']

            ##判断用户原密码是否匹配
            user = User.objects.filter(username=username)
            if user:
                user = User.objects.get(username=username)

                if user.check_password(oldpassword)==True:

                    user.set_password(newpassword)
                    user.save()
                    info = '密码修改成功!'
                else:
                    info = '请检查原密码是否输入正确!'
            elif len(user) == 0:
                info = '请检查用户名是否正确!'

        return HttpResponse(info)
    else:
        uf = ChangeForm()
    return render(request,'news/change.html', {'uf': uf})
def active_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        user = User.objects.filter(username=username)
        if user:
           user=User.objects.get(username=username)
           if user.is_active==True:
               message = '账户已被激活，无需再次激活,或已被他人注册！'
           else:
               message = '对不起，验证链接已经过期，请重新注册'
               user.delete()
        else:
            message='账户不存在，请重新注册'
        return render(request, 'news/message.html', {'message': message})
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        message='对不起，验证链接已经过期，请重新注册'
        return render(request, 'news/message.html', {'message':message})
    user.is_active = True
    user.save()

    return HttpResponseRedirect("/accounts/login/")