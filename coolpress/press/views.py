import datetime

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    now = datetime.datetime.now()
    html = "<html><body><h1>welcome to coolpress</h1></body></html>"
    return HttpResponse(now, html)