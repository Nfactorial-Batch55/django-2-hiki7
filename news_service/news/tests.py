from django.test import TestCase
from .models import News, Comment


class NewsModelTests(TestCase):

    def setUp(self):
        self.news_with_comments = News.objects.create(title='news with comments', content='content1')
        Comment.objects.create(news=self.news_with_comments, content='comment1')

        self.news_without_comments = News.objects.create(title='news without comments', content='content2')

    def test_has_comments_true(self):
        self.assertTrue(self.news_with_comments.has_comments())

    def test_has_comments_false(self):
        self.assertFalse(self.news_without_comments.has_comments())
