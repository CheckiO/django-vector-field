# Create your views here.
from django.shortcuts import render
from models import Task

def home(request):
    tasks = Task.objects.all()
    for t in tasks:
        print t.logo
        print t.logo.small.url, t.logo.big_log.url
    print(tasks)
    return render(request, "base.html", locals())

