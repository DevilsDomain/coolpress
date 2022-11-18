import datetime
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import join
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView
from rest_framework.templatetags.rest_framework import data

from press.forms import CommentForm, PostForm, NewCategory
from press.models import Category, Post, Comment, CoolUser
from django.contrib import messages


def home(request):
    now = datetime.datetime.now()
    msg = 'Welcome to Coolpres'
    categories = Category.objects.all()
    latest = Post.objects.order_by('-id')[:5]
    user = request.user
    li_cats = [f'<li>{cat.label}</li>' for cat in categories]
    cats_ul = f'<ul>{"".join(li_cats)}</ul>'

    html = f"<html><head><title>{msg}</title><body><h1>{msg}</h1><div>{user}</div><p>It is now {now}.</p>{cats_ul}</body></html>"
    return HttpResponse(html)


def render_a_post(post):
    return f'<div style="margin: 20px;padding-bottom: 10px;"><h2>{post.title}</h2><p style="color: gray;">{post.body}</p><p>{post.author.user.username}</p></div>'


# def create_new_category(request, user_id):
#     user = CoolUser.objects.get(user_id=user_id)
#     return render(request, 'new_category.html')


def create_new_category(request):
    form = NewCategory(request.POST)
    if request.method == "POST":
        if form.is_valid():
            label = form.cleaned_data.get('label')
            slug = form.cleaned_data['slug']
            Category.objects.create(label=label, slug=slug, created_by=request.user.cooluser)
    form = NewCategory()
    return render(request, "new_category.html", {'form': form})


def posts_list(request):
    objects = Post.objects.all()[:20]
    return render(request, 'posts_list.html', {'posts_list': objects})


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    data = request.POST or {'votes': 10}
    form = CommentForm(data)
    comments = post.comment_set.order_by('-creation_date')
    return render(request, 'posts_detail.html', {'post_obj': post, 'comment_form': form, 'comments': comments})


@login_required
def add_post_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    data = request.POST or {'votes': 10}
    form = CommentForm(data)
    if request.method == 'POST':
        if form.is_valid():
            votes = form.cleaned_data.get('votes')
            body = form.cleaned_data['body']
            Comment.objects.create(votes=votes, body=body, post=post, author=request.user.cooluser)
            return HttpResponseRedirect(reverse('posts-detail', kwargs={'post_id': post_id}))

    return render(request, 'comment-add.html', {'form': form, 'post': post})


@login_required
def post_update(request, post_id=None):
    post = None
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        if request.user != post.author.user:
            return HttpResponseBadRequest('Not allowed to change others posts')

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            username = request.user.username
            instance.author = CoolUser.objects.get(user__username=username)
            instance.save()
            return HttpResponseRedirect(reverse('posts-detail', kwargs={'post_id': instance.id}))
    else:
        form = PostForm(instance=post)

    return render(request, 'posts_update.html', {'form': form})


def HomePage(request):
    posts = Post.objects.order_by('-id')[:5]
    cats = Category.objects.all()
    return render(request, 'home_page.html', {'posts': posts, 'cats': cats})


class AuthorListView(ListView):
    query1 = User.objects.all()
    query2 = CoolUser.objects.all()
    queryset = list(chain(query1, query2))
    paginate_by = 10
    template_name = 'author_list.html'


class AuthorPosts(View):
    def get(self, request):
        objects = Post.objects.filter(author_id=request.user.cooluser)
        return render(request, 'author_posts_list.html', {'posts_list': objects})