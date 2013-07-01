# Create your views here.
from django.shortcuts import render
from models import TestM


def home(request):
    images = TestM.objects.all()
    for i in images:
        print i.image
    return render(request, "base.html", locals())

