from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def soon(request):
    return render(request, 'main/soon.html')