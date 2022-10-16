from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from .models import (
    Genre, 
    Book,
    Author,
    Review,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from follow.models import Follow
from orders.views import CartMixin
from django.contrib import messages
from .forms import ReviewForm
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
# Create your views here.


class IndexView(CartMixin, generic.ListView):
    template_name = 'index.html'
    models = Book
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        return Book.published.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        genres = Genre.objects.all()
        context['genres'] = genres
        return context


class GetReview(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm
        book = Book.published.get(slug=self.kwargs['slug'])
        review_user = book.book_reviews.filter(user__username=self.request.user)
        context['exist'] = review_user
        book_visit_count = self.request.session.get('book_visit_count', 0)
        newCount = book_visit_count + 1
        self.request.session['book_visit_count'] = newCount
        context['newCount']=newCount
        return context
    
    def get_queryset(self):
        return Book.published.filter(slug=self.kwargs['slug'])


class PostReview(SingleObjectMixin, LoginRequiredMixin, generic.FormView):
    model = Book
    form_class = ReviewForm
    context_object_name = 'book'
    template_name = 'book_detail.html'

    def get_queryset(self):
        return Book.published.filter(slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        review_all = Review.objects.filter(user=self.request.user)
        for review_obj in review_all:
            if review_obj.book == Book.objects.get(slug=self.kwargs['slug']):
                raise PermissionDenied(messages.add_message(self.request, messages.ERROR, "User Cannot add review second time"))
        comment = form.save(commit=False)
        comment.book = self.object
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        book = self.object
        return reverse('shop:book_detail', args=[book.slug])


class BookDetailView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        view = GetReview.as_view()
        return view(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        view = PostReview.as_view()
        return view(request, *args, **kwargs)

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
        author_visit_count = request.session.get('author_visit_count', 0)
        newCount = author_visit_count + 1
        request.session['author_visit_count'] = newCount
        context = {
            'author':author,
            'following_status':following_status,
            'followers_count':followers_count,
            'newCount':newCount,
        }
        return render(request, self.template_name, context)

class GenreBookView(CartMixin, generic.ListView):
    model = Genre
    template_name = 'book_by_genre.html'
    context_object_name = 'books'
    paginate_by = 2

    def get_queryset(self):
        genre = Genre.objects.get(slug=self.kwargs['slug'])
        books = genre.book_set.all()
        return books
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        genres = Genre.objects.all()
        context['genres'] = genres
        return context

class AddToWishlist(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=self.kwargs['book_id'])
        if book.users_wishlist.filter(id=request.user.id):
            book.users_wishlist.remove(request.user)
            messages.success(self.request, "Successfully Removed From Wishlist")
            return redirect('shop:index')
        else:
            book.users_wishlist.add(request.user)
            messages.success(self.request, "Successfully Added to Wishlist")
            return redirect('shop:index')


class SearchView(View):
    template_name = 'search/search.html'
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        search = Book.published.filter(
            Q(title__icontains=query) | Q(description__icontains=query) |
            Q(author__first_name__icontains = query) | Q(author__last_name__icontains=query) |
            Q(author__description__icontains = query) |
            Q(genre__genre__icontains=query) | Q(language__language__icontains=query) |
            Q(publisher__name__icontains=query) | Q(publisher__website__icontains=query)
        )
        search_author = Author.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(description__icontains=query)
        )
        context = {
            'search':search,
            'search_author':search_author,
        }
        return render(request, self.template_name, context)