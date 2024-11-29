from django.shortcuts import render
from .models import ShimlaAttraction

def index(request):
    attractions = ShimlaAttraction.objects.all()
    return render(request, 'index.html', {'attractions': attractions})
