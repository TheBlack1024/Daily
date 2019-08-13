#coding=utf-8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import ListView
from django.db.models import Q
from django.urls import reverse


from .models import Daily,Employees
from .form import DailyForm
"""
def index(request):
    dailys = Daily.objects.all()
    context = {
        'dailys': dailys,
    }
    return render(request,'index.html',context)
"""

class IndexView(ListView):
    model = Daily
    paginate_by = 5
    context_object_name = 'daily_list'
    template_name = 'index.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.session.get('company_id',None)
        if not company_id:
            return queryset.filter(owner__company__id = 0)
        return queryset.filter(owner__company__id=company_id)
        
        
def detail(requset,daily_id):
    daily = get_object_or_404(Daily,pk=daily_id)
    context = {
        'daily': daily,
    }
    return render(requset,'daily/detail.html',context)

class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword','')
        })
        return context

    def get_queryset(self):
        querset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return querset
        return querset.filter(Q(title__icontains=keyword) | Q(owner__name__icontains=
                                                              keyword))


class AuthorView(IndexView):
    """
    按汇报人查询
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id = author_id)

class CompanyView(IndexView):
    """
    按公司查询
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.kwargs.get('company_id')
        return queryset.filter(owner__company_id = company_id)


def results(request):
    """日报提交"""
    if request.method == 'POST':
        form = DailyForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.owner = Employees.objects.get(user__id=request.session.get('user_id',None))
            result.save()
            return HttpResponseRedirect(reverse('daily:index'))
    else:
        form = DailyForm()

    return render(request,'daily/results.html',locals())
