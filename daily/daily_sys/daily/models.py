#coding=utf-8
from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Company(models.Model):

    name = models.CharField(max_length=255,verbose_name='公司名')
    introduce = models.TextField(verbose_name='公司的介绍')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='建组时间')
    owner = models.ForeignKey('Employees',verbose_name='建组人',on_delete=models.CASCADE,related_name='company_founder')

    class Meta:
        verbose_name = verbose_name_plural = '公司'

    def __str__(self):
        return self.name

class Employees(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='em_user',verbose_name='员工账号',)
    name = models.CharField(max_length=255,verbose_name='员工姓名',null=True,blank=True)
    company = models.ForeignKey(Company,verbose_name='所属公司',on_delete=models.CASCADE,null=True,blank=True,related_name='company_employees')

    #接受保存模型的信号处理方法，只要是User调用了save方法，那么就会创建一个UserExtension和User进行绑定。
    """
    @receiver(post_save, sender=User)
    def create_user_extension(sender, instance, created, **kwargs):
        if created:
            Employees.objects.create(user=instance)
        else:
            instance.em_user.save()
    """
    class Meta:
        verbose_name = verbose_name_plural = '员工'

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.user.username


class Tag(models.Model):

    name = models.CharField(max_length=255,verbose_name='标签名')
    owner = models.ForeignKey(Employees,verbose_name='创建人',on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name

class Category(models.Model):

    name = models.CharField(max_length=255,verbose_name='类名')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    owner = models.ForeignKey(Employees,verbose_name='创建人',on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

class Daily(models.Model):

    title = models.CharField(max_length=255,verbose_name='标题')
    owner = models.ForeignKey(Employees,verbose_name='汇报人',on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='日报创建时间')
    tag = models.ManyToManyField(Tag,verbose_name='标签')
    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)
    content = RichTextUploadingField(verbose_name='日报')

    class Meta:
        verbose_name = verbose_name_plural = "日报"
        ordering = ['-created_time']

    def __str__(self):
        return self.title
    



