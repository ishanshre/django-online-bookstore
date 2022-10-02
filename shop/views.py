from django.shortcuts import render
from django.views import generic
from .models import Genre, Book
# Create your views here.


class IndexView(generic.TemplateView):
    template_name = 'index.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        genres = Genre.objects.all()
        books = Book.published.all()
        context['genres'] = genres
        context['books'] = books
        return context


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book_detail.html'