from __future__ import unicode_literals

import shutil
from os import path

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode


def upload_location(instance, filename):
    return path.join(instance.post.slug, filename)


class CategoriesModel(models.Model):
    name = models.CharField(max_length=100)
    canlist = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class PostModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(CategoriesModel, default=1)
    slug = models.CharField(max_length=2000, unique=True, blank=True)
    content = models.TextField(default=None)
    canlist = models.BooleanField(default=True)
    can_duoshuo = models.BooleanField(default=True)
    draft = models.BooleanField(default=False)
    createtime = models.DateTimeField(auto_now=False, auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True, auto_now_add=False)
    publishtime = models.DateTimeField(default=timezone.now, auto_now=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-publishtime', '-updatetime']


class ImageModle(models.Model):
    post = models.ForeignKey(PostModel)
    image = models.ImageField(upload_to=upload_location, blank=True)


def create_slug(instance, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(unidecode(instance.title))
    qs = PostModel.objects.filter(slug=slug)
    if qs.exists():
        new_slug = '%s-%s' % (slug, qs.first().id)
        return create_slug(instance, new_slug)
    return slug


def pre_save_signal_PostModel_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


def pre_delete_signal_PostModel_receiver(sender, instance, *args, **kwargs):
    shutil.rmtree(path.join(settings.MEDIA_ROOT, instance.slug), ignore_errors=True)


pre_delete.connect(pre_delete_signal_PostModel_receiver, sender=PostModel)
pre_save.connect(pre_save_signal_PostModel_receiver, sender=PostModel)
