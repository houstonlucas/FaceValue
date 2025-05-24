from django.shortcuts import render

def home(request):
    """
    Render homepage using template extending base layout.
    """
    return render(request, 'home.html')