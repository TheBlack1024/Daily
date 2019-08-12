#coding=utf-8
from django.contrib import admin

from .models import Daily,Company,Category,Employees,Tag
"""
class DailyAdmin(admin.ModelAdmin):
    list_display = ['title','owner','created_time','_company']
    list_filter = ['created_time']
    search_fields = ['title','tag','owner']
    fieldsets = [
        ('Daily', {
            'fields': ['title','owner','content','tag','category'],
        }),
    ]

    def _company(self,obj):
        return obj.owner.company
admin.site.register(Daily,DailyAdmin)
"""
#自定义过滤除了超级用户用户只能看到自己的内容
class DailyAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,form,change):
        if not obj.id:
            obj.owner = Employees.objects.get(user=request.user)
        obj.save()

    def get_form(self,request,obj=None,**kwargs):
        self.exclude = ("user",)
        form = super(DailyAdmin,self).get_form(request, obj, **kwargs)
        return form

    list_display = ['title','owner','created_time','_company']
    list_filter = ['created_time']
    search_fields = ['title','owner__name',]
    #list_display_links =['owner',]
    #exclude = ('owner',)
    fieldsets = [
        ('Daily', {
            'fields': ['title','content','tag','category'],
        }),
    ]
    filter_horizontal = ('tag',)
    readonly_fields = ('owner',)

    def get_queryset(self,request):
        """当前用户内容限制"""
        qs = super(DailyAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner__user=request.user)

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    def _company(self,obj):
        return obj.owner.company


admin.site.register(Daily,DailyAdmin)



class TagAdmin(admin.ModelAdmin):
    def save_model(self,request,obj,form,change):
        if not obj.id:
            obj.owner = Employees.objects.get(user=request.user)
        obj.save()

    def get_form(self,request,obj=None,**kwargs):
        self.exclude = ("user",)
        form = super(TagAdmin,self).get_form(request, obj, **kwargs)
        return form

    list_display = ['name','owner','created_time']
    list_filter = ['created_time']
    search_fields = ['name']
    fieldsets = [
        ('Tag', {
            'fields': ['name',],
        }),
    ]

    def get_queryset(self,request):
        qs = super(TagAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner__user=request.user)
admin.site.register(Tag,TagAdmin)


class CompanyAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.owner = Employees.objects.get(user=request.user)
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user",)
        form = super(CompanyAdmin, self).get_form(request, obj, **kwargs)
        return form

    list_display = ['name','introduce','created_time','owner',]
    list_filter = ['created_time',]
    search_fields = ['name']
    fieldsets = [
        ('company',{
            'fields': ['name','introduce',]
        }),
    ]
    def get_queryset(self,request):
        qs = super(CompanyAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=Employees.objects.get(user=request.user))
admin.site.register(Company,CompanyAdmin)

class CategoryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.owner = Employees.objects.get(user=request.user)
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("user",)
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        return form

    list_display = ['name', 'created_time', 'owner', ]
    list_filter = ['created_time', ]
    search_fields = ['name']
    fieldsets = [
        ('category', {
            'fields': ['name',]
        }),
    ]
    def get_queryset(self,request):
        qs = super(CategoryAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner__user=request.user)
admin.site.register(Category, CategoryAdmin)

class EmployeesAdmin(admin.ModelAdmin):

    list_display = ['name','company','user']
    #list_filter = []
    search_fields = ['name']
    fieldsets = [
        ('employees', {
            'fields': ['name','company','user']
        }),
    ]
admin.site.register(Employees, EmployeesAdmin)
    