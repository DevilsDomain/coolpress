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

