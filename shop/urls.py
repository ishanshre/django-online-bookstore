from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('book_detail/<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('author/<slug:slug>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('book/<int:pk>/', views.GenreBookView.as_view(), name='book_by_genre'),
    path('add_to_wishlist/<int:book_id>/', views.AddToWishlist.as_view(), name='add_to_wishlist'),
]