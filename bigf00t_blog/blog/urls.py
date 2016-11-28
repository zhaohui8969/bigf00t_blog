from django.conf.urls import url

from .views import posts_list, posts_create, posts_detail, posts_edit, posts_delete, category_list

urlpatterns = [
    url(r'^$', posts_list, name='list'),
    url(r'^create$', posts_create, name='create'),
    url(r'^categories$', category_list, name='categories'),
    url(r'^(?P<slug>[\w-]+)/$', posts_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', posts_edit, name='edit'),
    url(r'^(?P<slug>[\w-]+)/delete/$', posts_delete, name='delete'),
]
