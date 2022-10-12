from django.shortcuts import render
from django.views import generic, View
from .models import (
    Genre, 
    Book,
    Author,
)
from follow.models import Follow
from orders.views import CartMixin
# Create your views here.


class IndexView(CartMixin, generic.TemplateView):
    template_name = 'index.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        genres = Genre.objects.all()
        books = Book.published.all()
        context['genres'] = genres
        context['books'] = books
        return context


class BookDetailView(CartMixin, generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book_detail.html'


# class AuthorDetailView(generic.DetailView):
#     model = Author
#     context_object_name = 'author'
#     template_name = 'author_detail.html'

class AuthorDetailView(CartMixin, View):
    template_name = 'author_detail.html'
    def get(self, request, *args, **kwargs):
        author = Author.objects.get(slug=self.kwargs['slug'])
        followers = Follow.objects.all()
        followers_count = Follow.objects.filter(followed=author).count()
        following_status = False
        if request.user.is_authenticated:
            if followers.filter(followed_by=request.user, followed=author):
                following_status = True

        context = {
            'author':author,
            'following_status':following_status,
            'followers_count':followers_count,
        }
        return render(request, self.template_name, context)

class GenreBookView(CartMixin, generic.TemplateView):
    template_name = 'book_by_genre.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        genre = Genre.objects.get(id=self.kwargs['pk'])
        context['genre'] = genre
        return context
