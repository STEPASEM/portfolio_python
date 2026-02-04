from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('add_comment/<int:id>/', views.AddComment.as_view(), name='add_comment'),
    path('category/<str:category_slug>/', views.CategoryView.as_view(), name='category_posts'),
    path('create/', views.CreatePost.as_view(), name='create_post'),
    path('profile/edit/', views.EditProfile.as_view(), name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:id>/edit/', views.EditPost.as_view(), name='edit_post'),
    path('posts/<int:id>/delete/', views.DeletePost.as_view(), name='delete_post'),
    path('posts/<int:post_id>/comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('posts/<int:post_id>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]