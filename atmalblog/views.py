import json
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from atmal_blog.settings import MEDIA_ROOT
from .forms import *


def _get_initial_form_set_data():
    return [{'name': '', 'language': lang} for lang in Language.objects.all()]


def index(request):
    context = {
        'posts': PostTranslations.objects.order_by('-published_date'),
    }
    return render(request, 'posts-list.html', context=context)


@staff_member_required
def new_post(request):
    if request.method == 'POST':
        # Series and category forms are handled by other view functions.
        # Here, we only deal with the post form.

        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            # Create post
            categories = post_form.cleaned_data['categories']
            series = post_form.cleaned_data['series']
            thumbnail = post_form.cleaned_data['thumbnail']
            post = Post.objects.create(series=series, thumbnail=thumbnail)
            post.categories.set(categories)

            # Create translation
            title = post_form.cleaned_data['title']
            short_desc = post_form.cleaned_data['short_description']
            content = post_form.cleaned_data['content']
            language = Language.objects.get(native_name=post_form.cleaned_data['language'])
            PostTranslations.objects.create(post=post,
                                            title=title,
                                            short_description=short_desc,
                                            content=content,
                                            language=language)
            return redirect('index')
    else:
        post_form = PostForm()

    context = {
        'post_form': post_form,
        'series_translation_form_set': SeriesTranslationFormSet(initial=_get_initial_form_set_data()),
        'category_translation_form_set': CategoryTranslationFormSet(initial=_get_initial_form_set_data()),
    }

    return render(request, 'new_post.html', context=context)


@staff_member_required
def new_translation_post_select(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'new_translation_post_select.html', context)


def new_translation(request, pk):
    context = {
        'post_form': PostTranslationForm(),
    }

    raise NotImplementedError()


@staff_member_required
@require_http_methods(['POST'])
def new_post_cleanup(request):
    """
    This view function will be called by navigator.sendBeacon when user
    leaves the /new-post page but is not submitting the form, and has
    uploaded files via markdownx (markdown editor) that are unused.

    Therefore, to prevent these files from piling up, this view will be
    used to delete them.
    :param request: POST form request with a list of files to delete
    :return: HTTP Response 200
    """
    files = json.loads(request.POST['files'])
    for file in files:
        file_path = os.path.join(MEDIA_ROOT, file.lstrip('/'))
        os.remove(file_path)
    return HttpResponse()


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


@staff_member_required
@require_http_methods(['POST'])
def new_category(request):
    form_set = CategoryTranslationFormSet(request.POST, initial=_get_initial_form_set_data())

    if form_set.is_valid():
        category = Category.objects.create()
        for form in form_set:
            form_name = form.cleaned_data['name']
            form_lang = Language.objects.get(native_name=form.cleaned_data['language'])
            CategoryTranslation.objects.create(category=category, name=form_name, language=form_lang)

        response = {
            'pk': category.pk,
            'str': str(category)
        }
        return JsonResponse(response)
    else:
        return JsonResponse({'errors': form_set.errors}, status=400)


def view_post(request, pk, slug):
    post = PostTranslations.objects.get(pk=pk)
    series = SeriesTranslations.objects.get(series=post.post.series, language=post.language)
    context = {
        'post': post,
        'series': series,
    }
    return render(request, 'post.html', context)


@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('index')
