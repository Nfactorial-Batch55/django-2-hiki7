from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .models import News, Comment
from .forms import CommentForm


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(news=self.object).order_by('-created_at')
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        news = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.save()
        return redirect('news-detail', pk=news.pk)


class NewsCreateView(CreateView):
    model = News
    template_name = 'news/news_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.created_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('news-detail', kwargs={'pk': self.object.pk})
