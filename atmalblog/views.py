from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, 'index.html')


@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('index')
