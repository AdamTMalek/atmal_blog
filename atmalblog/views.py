from django.contrib.auth import logout
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, 'index.html')


@staff_member_required
def new_post(request):
    return render(request, 'new_post.html')


@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('index')
