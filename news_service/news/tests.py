from django.test import TestCase
from .models import News, Comment

from django.urls import reverse


class NewsModelTests(TestCase):

    def setUp(self):
        self.news_with_comments = News.objects.create(title='news with comments', content='content1')
        Comment.objects.create(news=self.news_with_comments, content='comment1')

        self.news_without_comments = News.objects.create(title='news without comments', content='content2')

    def test_has_comments_true(self):
        self.assertTrue(self.news_with_comments.has_comments())

    def test_has_comments_false(self):
        self.assertFalse(self.news_without_comments.has_comments())


class NewsViewTests(TestCase):

    def setUp(self):
        self.news = News.objects.create(title='news', content='content')
        self.comment1 = Comment.objects.create(news=self.news, content='comment1')
        self.comment2 = Comment.objects.create(news=self.news, content='comment2')

    def test_news_list_view(self):
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_list.html')
        self.assertContains(response, self.news.title)
        self.assertQuerysetEqual(
            response.context['news_list'],
            News.objects.order_by('-created_at'),
            transform=lambda x: x
        )

    def test_news_details_view(self):
        response = self.client.get(reverse('news-detail', args=[self.news.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_detail.html')
        self.assertContains(response, self.news.title)
        self.assertContains(response, self.comment1.content)
        self.assertContains(response, self.comment2.content)

    def test_news_comments_sorted(self):
        response = self.client.get(reverse('news-detail', args=[self.news.pk]))
        comments = list(response.context['comments'])
        self.assertEqual(comments[0].content, self.comment2.content)
        self.assertEqual(comments[1].content, self.comment1.content)
