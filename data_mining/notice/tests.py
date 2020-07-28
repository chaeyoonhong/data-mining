from django.shortcuts import render
from django.http import HttpResponse
from .models import KeywordTable
from django.db.models import Q
from django import forms