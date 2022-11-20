from django.test import TestCase

# Create your tests here.
from press.models import Comment, CommentStatus, User, CoolUser, Post, Category


class CommentsModeration(TestCase):
    # check that the comment is PUBLISHED by default when creates
    def test_comment_status(self):
        user = User.objects.create(username='pepito')
        cu = CoolUser.objects.create(user=user)
        cat = Category.objects.create(label='cat', slug='cat', created_by=cu)
        post = Post.objects.create(title='title', body='body', author=cu, category=cat)
        comment = Comment.objects.create(body='test comment', author=cu, votes=2, post=post)
        comment.save()
        self.assertIs(comment.status, CommentStatus.PUBLISHED)

    # check that the comment is indeed added to the post_details
    def test_comment_added(self):
        user = User.objects.create(username='pepito')
        cu = CoolUser.objects.create(user=user)
        cat = Category.objects.create(label='cat', slug='cat', created_by=cu)
        post = Post.objects.create(title='title', body='body', author=cu, category=cat)
        comment = Comment.objects.create(body='test comment', author=cu, votes=2, post=post)
        comment.save()
        response = self.client.get('/post_details/1')
        self.assertContains(response, '<p>No comments added yet<p>', 0)

    def test_comment_status_in_posts_details(self):
        user = User.objects.create(username='pepito')
        cu = CoolUser.objects.create(user=user)
        cat = Category.objects.create(label='cat', slug='cat', created_by=cu)
        post = Post.objects.create(title='title', body='body', author=cu, category=cat)
        comment = Comment.objects.create(body='test comment', author=cu, votes=2, post=post,
                                         status=CommentStatus.NON_PUBLISHED)

        comment.save()
        response = self.client.get('/post_details/1')
        self.assertContains(response, '<p>No comments added yet<p>', 1)


class TrendingPage(TestCase):

    def test_trending_post_default(self):
        # creating a post
        response = self.client.get('/trending/')
        user = User.objects.create(username='pepito')
        cu = CoolUser.objects.create(user=user)
        cat = Category.objects.create(label='cat', slug='cat', created_by=cu)
        post = Post.objects.create(title='title', body='body', author=cu, category=cat)
        post.save()
        # by default the post shouldn't be in trending posts
        self.assertContains(response, '<div class="card mb-3 post">', 0)

    def test_trending_post(self):
        response = self.client.get('/trending/')
        user = User.objects.create(username='pepito')
        cu = CoolUser.objects.create(user=user)
        cat = Category.objects.create(label='cat', slug='cat', created_by=cu)
        post = Post.objects.create(title='title', body='body', author=cu, category=cat)
        post.save()
        #  post should be on the trending page
        for i in range(10):
            comment = Comment.objects.create(body='test comment', author=cu, votes=2, post=post)
            comment.save()
        self.assertContains(response,
                            '<p class="text-center font-weight-bold">There are no posts yet for this category, let' + "'s create some :D</p>",
                            0)
