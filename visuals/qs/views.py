from django.shortcuts import render

# Create your views here.

def intro(request):
    return render(request, 'intro.html')

def methods(request):
    return render(request, 'methods.html')

def background(request):
    return render(request, 'background.html')

def academics(request):
    return render(request, 'academics.html')

def postgrad(request):
    return render(request, 'postgrad.html')

def discrimination(request):
    return render(request, 'discrimination.html')

def belonging(request):
    return render(request, 'belonging.html')

def conclusion(request):
    return render(request, 'conclusion.html')
