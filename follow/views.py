from django.shortcuts import render, get_object_or_404, redirect
from .models import Follow
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from shop.models import Author
# Create your views here.

class AddFollow(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        slug=self.kwargs['slug']
        followed = get_object_or_404(Author, slug=self.kwargs['slug'])
        followed_by = get_object_or_404(get_user_model(), id = request.user.id)

        follow = Follow.objects.create(
            followed = followed,
            followed_by = followed_by
        )
        follow.save()
        return redirect('shop:author_detail', slug)
            
class RemoveFollow(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        slug=self.kwargs['slug']
        followed = get_object_or_404(Author, slug=self.kwargs['slug'])
        followed_by = get_object_or_404(get_user_model(), id = request.user.id)

        follow = Follow.objects.get(
            followed = followed,
            followed_by = followed_by
        )
        follow.delete()
        return redirect('shop:author_detail', slug)
