#coding:utf8
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
class Zlzp(models.Model):
    gsmc=models.CharField('公司名称',max_length=100,unique=True)
    gsjj=models.TextField('公司简介',max_length=254)
    #gssulg=models.CharField('公司网址',max_length=100)
    nav_display = models.BooleanField('导航显示', default=False)
    home_display = models.BooleanField('首页显示', default=False)
    def __str__(self):
        return self.gsmc
    class Meta:
        verbose_name='招聘公司'
        verbose_name_plural='招聘公司'
        ordering=['gsmc']
    def get_absolute_url(self):
        return reverse('gsmc', args=(self.gsmc,))
class Zwxx(models.Model):
    gsmcc=models.ManyToManyField(Zlzp, verbose_name='招聘公司')

    #title=models.CharField('标题',max_length=254)
    zwmc=models.CharField('职位名称',max_length=100)
    zwyx=models.CharField('职位月薪',max_length=100)

    gzdd=models.CharField('工作地点',max_length=100)
    gsmz=models.CharField('公司名称',max_length=100)
    zwjj=models.TextField('职位要求', max_length=254)
    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)
    published = models.BooleanField('正式发布', default=True)
    def __str__(self):
        return self.zwmc
    class Meta:
        verbose_name='职位名称'
        verbose_name_plural='职位名称'
        ordering=['zwmc']
    def get_absolute_url(self):
        return reverse('zwxx', args=(self.pk,))



