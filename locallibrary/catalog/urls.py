from django.urls import path
from django.conf.urls.i18n import set_language
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('i18n/setlang/', set_language, name='set_language'),
]
