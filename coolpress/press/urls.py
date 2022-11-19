from django.urls import path, re_path
from press import views
from press.views import AuthorListView, AuthorPosts, AuthorsViewSet
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'authors', views.AuthorsViewSet)

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

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
