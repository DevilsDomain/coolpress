from django.urls import path
from press import views
from press.views import AuthorListView, AuthorPosts

urlpatterns = [
    path('posts/', views.posts_list, name='posts-list'),
    path('post_details/<int:post_id>', views.post_detail, name='posts-detail'),
    path('post/<int:post_id>/comment-add/', views.add_post_comment, name='comment-add'),
    path('post/update/<int:post_id>', views.post_update, name='post-update'),
    path('post/add/', views.post_update, name='post-add'),
    path('add/category/', views.create_new_category, name='new-category'),
    path('home/', views.HomePage, name='category-list'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/posts/', AuthorPosts.as_view(), name='author-posts'),

]
