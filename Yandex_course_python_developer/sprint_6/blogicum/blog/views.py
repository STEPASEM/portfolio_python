from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from zmq.decorators import context

from blog.models import Post, Category

def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.all().filter(
        pub_date__lte=timezone.now(),
        category__is_published=True,
        is_published=True).order_by('-pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, template, context)

def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(
        slug=category_slug,
        is_published=True
        )
    )
    posts = category.post_set.filter(
        pub_date__lte=timezone.now(),
        is_published=True
    )
    context = {'category': category, 'post_list': posts}
    return render(request, template, context)

def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ),
    pk=id
    )
    context = {'post': post}
    return render(request, template, context)

