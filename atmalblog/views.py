from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from .forms import *


def _get_initial_form_set_data():
    return [{'name': '', 'language': lang} for lang in Language.objects.all()]


def index(request):
    return render(request, 'index.html')


@staff_member_required
def new_post(request):
    if request.method == 'POST':
        pass

    context = {
        'post_form': PostForm(),
        'series_translation_form_set': SeriesTranslationFormSet(initial=_get_initial_form_set_data()),
        'category_translation_form_set': CategoryTranslationFormSet(initial=_get_initial_form_set_data()),
    }

    return render(request, 'new_post.html', context=context)


@staff_member_required
@require_http_methods(['POST'])
def new_series(request):
    form_set = SeriesTranslationFormSet(request.POST, initial=_get_initial_form_set_data())

    if form_set.is_valid():
        series = Series.objects.create()
        for form in form_set:
            form_name = form.cleaned_data['name']
            form_lang = Language.objects.get(native_name=form.cleaned_data['language'])
            SeriesTranslations.objects.create(series=series, name=form_name, language=form_lang)

        response = {
            'pk': series.pk,
            'str': str(series)
        }
        return JsonResponse(response)
    else:
        return JsonResponse({'errors': form_set.errors}, status=400)


@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('index')
