from django.http import HttpResponse
from django.shortcuts import render
import datetime

# Create your views here.

def index(request):
    now = datetime.datetime.now()
    return render(request , "birthday/index.html", {
        "birthday": now.month == 10 and now.day == 17
    })