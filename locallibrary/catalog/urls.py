from django.urls import path
from django.conf.urls.i18n import set_language
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('i18n/setlang/', set_language, name='set_language'),
]
