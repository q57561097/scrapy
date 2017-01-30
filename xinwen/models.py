#coding: utf-8
from django.core.urlresolvers import reverse

from django.db import models




class Colum(models.Model):
    name = models.CharField('栏目名称', max_length=100)
    slug = models.CharField('栏目网址', max_length=100, db_index=True)
    intro = models.TextField('栏目简介', default='',blank=True)
    nav_display = models.BooleanField('导航显示', default=False)
    home_display = models.BooleanField('首页显示', default=False)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '栏目1'
        verbose_name_plural = '栏目2'
        ordering = ['name']  # 按照哪个栏目排序

    def get_absolute_url(self):
        return reverse('colu', args=(self.slug,))


class Articl(models.Model):
    column = models.ManyToManyField(Colum, verbose_name='归属栏目')

    title = models.CharField('标题', max_length=100)
    slug = models.CharField('网址', max_length=100, db_index=True)

    author = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者')
    content = models.TextField('内容', default='', blank=True)
    pub_date = models.DateTimeField('发表时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField('更新时间', auto_now=True, null=True)
    published = models.BooleanField('正式发布', default=True)

    def get_absolute_url(self):
        return reverse('arti', args=(self.pk, self.slug))
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '教程1'
        verbose_name_plural = '教程2'
