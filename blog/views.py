from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
  posts = Post.published.all()

  paginator = Paginator(posts, 10)
  page = request.GET.get('page')
  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)

  return render(request=request, template_name='post_list.html', context={'posts': posts})


def post_detail(request, post):
  post = get_object_or_404(Post, slug=post, status='published')
  return render(request=request, template_name='post_detail.html', context={'post': post})
