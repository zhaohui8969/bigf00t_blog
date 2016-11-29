# coding:utf-8
import os

from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, Http404, get_object_or_404, redirect

import user_auth
from blog_conf import common_conf
from .form import PostModelsForm, ImageModelsForm
from .models import PostModel, ImageModle, CategoriesModel


def posts_list(request):
    qs = PostModel.objects.filter(canlist=True)
    query_var = request.GET.get('q')
    if query_var:
        query_var_list = query_var.split(',')
        Q_condition = (Q(title__icontains=query_var_list[0]) |
                       Q(content__icontains=query_var_list[0]))
        if len(query_var_list) == 2:
            Q_condition = Q_condition & Q(category__name=query_var_list[1])
        qs = qs.filter(Q_condition
                       ).distinct()

    paginator = Paginator(qs, 20)  # Show 25 contacts per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        qs_paga = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        qs_paga = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        qs_paga = paginator.page(paginator.num_pages)

    content = {
        'common_conf': common_conf,
        'qs_paga': qs_paga,
        'page_request_var': page_request_var,
        'query_var': query_var,
        'page_name': 'index',
    }
    return render(request, 'index.html', content)


def posts_create(request):
    if not user_auth.check_login(request):
        raise Http404
    Image_Form_Set = modelformset_factory(ImageModle, form=ImageModelsForm)
    form = PostModelsForm(request.POST or None, request.FILES or None)
    image_form_set = Image_Form_Set(request.POST or None, request.FILES or None,
                                    queryset=ImageModle.objects.none())
    if form.is_valid() and image_form_set.is_valid():
        instance = form.save()

        for form in image_form_set.cleaned_data:
            if form.get('image'):
                image = form['image']
                photo = ImageModle(post=instance, image=image)
                photo.save()

        messages.success(request, 'create post')
        return HttpResponseRedirect(instance.get_absolute_url())
    content = {
        'form': form,
        'image_form_set': image_form_set,
        'sub_btn_var': 'Create',
    }
    return render(request, 'posts/posts_form.html', content)


def posts_detail(request, slug):
    obj = get_object_or_404(PostModel, slug=slug)
    content = {
        'common_conf': common_conf,
        'obj': obj,
    }
    qs = PostModel.objects.filter(publishtime__lt=obj.publishtime, canlist=True)
    if qs.exists():
        content['next_article'] = qs.first()
    qs = PostModel.objects.filter(publishtime__gt=obj.publishtime, canlist=True)
    if qs.exists():
        content['previous_article'] = qs.last()
    return render(request, 'article.html', content)


def posts_edit(request, slug):
    if not user_auth.check_login(request):
        raise Http404
    instance = get_object_or_404(PostModel, slug=slug)
    form = PostModelsForm(request.POST or None, request.FILES or None, instance=instance)
    Image_Form_Set = modelformset_factory(ImageModle, form=ImageModelsForm, can_delete=True)
    image_form_set = Image_Form_Set(request.POST or None, request.FILES or None,
                                    queryset=ImageModle.objects.filter(post=instance))
    if form.is_valid() and image_form_set.is_valid():
        instance = form.save()

        for form in image_form_set.cleaned_data:
            if form.get('id'):
                if form['DELETE']:
                    form['id'].delete()
                else:
                    image_instance = form['id']
                    if not image_instance.image == form['image']:
                        os.remove(os.path.join(settings.MEDIA_ROOT, str(image_instance.image)))
                    image_instance.image = form['image']
                    image_instance.save()
            elif form.get('image'):
                image = form['image']
                photo = ImageModle(post=instance, image=image)
                photo.save()

        messages.success(request, 'edit success')
        return HttpResponseRedirect(instance.get_absolute_url())
    content = {
        'form': form,
        'image_form_set': image_form_set,
        'sub_btn_var': 'Save',
    }
    return render(request, 'posts/posts_form.html', content)


def posts_delete(request, slug):
    if not user_auth.check_login(request):
        raise Http404
    try:
        instance = get_object_or_404(PostModel, slug=slug)
    except PostModel.DoesNotExist:
        return redirect('posts:list')
    instance.delete()
    messages.success(request, 'Delete 1 post')
    return redirect('posts:list')


def category_list(request):
    categories = CategoriesModel.objects.all()
    categories_list = [{'name': x.name, 'num': PostModel.objects.filter(category=x).count()} for x in categories if
                       not x.name == common_conf['not-list-category-name']]
    print categories_list
    content = {
        'common_conf': common_conf,
        'categories': categories_list,
        'page_name': 'categories',
    }
    return render(request, 'categories.html', content)
