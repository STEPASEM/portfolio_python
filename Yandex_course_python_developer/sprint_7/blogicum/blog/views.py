from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

User = get_user_model()


class CategoryView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        # Возвращаем посты этой категории
        return Post.objects.filter(
            category=category,
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем категорию в контекст
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return context

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')

class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['id'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'id': self.kwargs['id']})

    def get_context_data(self, **kwargs):
        # Добавляем пост в контекст
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['id'])
        return context

def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        ),
        pk=id
    )

    form = CommentForm()

    comments = post.comments.filter(is_published=True).order_by('created_at')

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, template, context)

def profile(request, username):
    # Получаем пользователя или 404
    profile = get_object_or_404(User, username=username)

    # Получаем посты пользователя
    posts = Post.objects.filter(
        author=profile,
        is_published=True,
        category__is_published=True
    ).order_by('-created_at')

    # Пагинация
    paginator = Paginator(posts, 10)  # 10 постов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = 'blog/profile.html'
    context = {
        'profile': profile,
        'page_obj': page_obj,
        'posts': posts,  # если нужно все посты без пагинации
    }
    return render(request, template, context)

class EditProfile(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})

    def get_object(self):
        # Редактируем текущего пользователя
        return self.request.user

class EditPost(LoginRequiredMixin, UpdateView):  # UpdateView вместо CreateView
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})

    def get_object(self):
        return get_object_or_404(
            Post,
            pk=self.kwargs['id'],
            author=self.request.user
        )


class DeletePost(LoginRequiredMixin, DeleteView):  # DeleteView вместо CreateView
    model = Post

    def get_success_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})

    def get_object(self):
        return get_object_or_404(
            Post,
            pk=self.kwargs['id'],
            author=self.request.user
        )

@login_required
def edit_comment(request, post_id=None, comment_id=None):
    if comment_id is not None:
        instance = get_object_or_404(
            Comment,
            pk=comment_id,
            author=request.user,
            post_id=post_id
        )
    else:
        instance = None

    # Создаем форму
    form = CommentForm(
        request.POST or None,
        instance=instance
    )

    context = {
        'form': form,
        'comment': instance,
        'post': instance.post if instance else None
    }

    # Если форма валидна, обрабатываем действие
    if form.is_valid():
        comment = form.save(commit=False)
        if not instance:  # Если это новый комментарий
            comment.author = request.user
            comment.post_id = post_id
        comment.save()
        return redirect('blog:post_detail', id=post_id)

    return render(request, 'blog/comment.html', context)

@login_required
def delete_comment(request, post_id=None, comment_id=None):
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        author=request.user,
        post_id=post_id
    )
    comment.delete()
    return redirect('blog:post_detail', id=post_id)