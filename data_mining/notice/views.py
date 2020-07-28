from django.shortcuts import render
from django.http import HttpResponse
from .models import KeywordTable
from django.db.models import Q
from django import forms
from .form import First
import operator

field=None
form=None
def rank(match):
    rank={}
    for data in match:
        if data.keyword in rank:
            rank[data.keyword]=rank[data.keyword]+data.count
        else:
            rank[data.keyword]=data.count
    rank = sorted(rank.items(),key=operator.itemgetter(1), reverse=True)
    if(len(rank)>19):
        rank=rank[0:19]
    return rank

def home(request):
    global field
    global form
    if request.method == 'POST' and 'search' in request.POST:
        site = request.POST["site"]
        first_date = request.POST["first_date"]
        last_date = request.POST["last_date"]
        if(field=='전체' and site=='전체' and first_date and last_date):
            match = KeywordTable.objects.filter(Q(date__range=(first_date, last_date)))
            word="SEARCH RESULTS ("+first_date+ " ~ "+last_date+')'
        elif (field and site and first_date and last_date):
            if(site=='전체'):
                match = KeywordTable.objects.filter( Q(type__icontains=field)& Q(date__range=(first_date, last_date)))
            else:
                match=KeywordTable.objects.filter(Q(type__icontains=field) & Q(site__icontains=site) &Q(date__range=(first_date,last_date)))
            word = "SEARCH RESULTS ("+ field+'  '+site+'  '+ first_date + " ~ " + last_date + ')'
        elif(field and site and not first_date and not last_date):
            if(site=='전체'):
                match = KeywordTable.objects.filter(Q(type__icontains=field))
                word = "SEARCH RESULTS (" + field + '  ' + site + ')'
                if(field=='전체'):
                    match=[]
                    word = "Your input is wrong. Check one more time."
            else:
                match = KeywordTable.objects.filter(Q(type__icontains=field) & Q(site__icontains=site))
                word = "SEARCH RESULTS (" + field + '  ' + site + ')'
        else:
            match=[]
            word="Your input is wrong. Check one more time."
        ranks = rank(match)
        if form.is_valid():
            field = form.cleaned_data['field']
            if (field=='언론사'):
                sites=["코인데스크코리아","디센터","블록미디어","조인디","코인니스","새우잡이"]
            elif (field=='커뮤니티'):
                sites=["코인판","코박","비트맨"]
            else:
                sites=[]
        return render(request, 'home.html', {'form': form, 'rank': ranks, 'word': word,'sites':sites})

    if request.method=='POST' and 'search' not in request.POST:
        form = First(request.POST or None)
        if form.is_valid():
            field = form.cleaned_data['field']
            if (field=='언론사'):
                sites=["코인데스크코리아","디센터","블록미디어","조인디","코인니스","새우잡이"]
            elif (field=='커뮤니티'):
                sites=["코인판","코박","비트맨"]
            else:
                sites=[]
        return render(request, 'home.html', {'form': form,'sites': sites})

    else:
        form=First()
        return render(request, 'home.html', {'form': form})