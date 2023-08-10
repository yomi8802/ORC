import os
from datetime import date
from typing import Any, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateForm, PostBulkDeleteForm
from .models import Post, DailyResult, SongResult
from .modules import recognition

class IndexView(LoginRequiredMixin, generic.TemplateView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    template_name = 'orc/index.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        queryset = Post.objects.filter(user=self.request.user)
        context['total_win_count'] = queryset.filter(winlose = 'WIN').count()
        context['total_lose_count'] = queryset.filter(winlose = 'LOSE').count()
        context['total_draw_count'] = queryset.filter(winlose = 'DRAW').count()
        context['total_count'] = queryset.all().count()
        context['total_AP_count'] = queryset.filter(AP = 'AP').count()
        if context['total_count'] != 0:
            context['total_win_ratio'] = round(context['total_win_count'] / context['total_count'] * 100,1)
            context['total_AP_ratio'] = round(context['total_AP_count'] / context['total_count'] * 100,1)
        else:
            context['total_win_ratio'] = 0
            context['total_AP_ratio'] = 0

        context['today_win_count'] = queryset.filter(winlose = 'WIN',date=timezone.now().date()).count()
        context['today_lose_count'] = queryset.filter(winlose = 'LOSE',date=timezone.now().date()).count()
        context['today_draw_count'] = queryset.filter(winlose = 'DRAW',date=timezone.now().date()).count()
        context['today_count'] = queryset.filter(date=timezone.now().date()).count()
        context['today_AP_count'] = queryset.filter(AP = 'AP', date=timezone.now().date()).count()
        if context['today_count'] != 0:
            context['today_win_ratio'] = round(context['today_win_count'] / context['today_count'] * 100,1)
            context['today_AP_ratio'] = round(context['today_AP_count'] / context['today_count'] * 100,1)
        else:
            context['today_win_ratio'] = 0
            context['today_AP_ratio'] = 0

        context['daily_results'] = DailyResult.objects.filter(user=self.request.user)
        context['song_results'] = SongResult.objects.filter(user=self.request.user)
        return context  

class PostListView(LoginRequiredMixin, generic.ListView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    form_class = PostBulkDeleteForm
    template_name = "orc/post_list.html"
    success_url = reverse_lazy('orc:post_list')

    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostBulkDeleteForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = PostBulkDeleteForm(request.POST)
        if form.is_valid():
            selected_ids = form.cleaned_data['selected_ids'].values_list('pk', flat=True)

            # 画像の削除処理を追加
            for post_id in selected_ids:
                try:
                    post = Post.objects.get(pk=post_id)
                    image_path = post.image.path
                    if os.path.exists(image_path):
                        os.remove(image_path)

                    #戦績を修正
                    #日付ごと
                    daily_result = DailyResult.objects.get(user=post.user, date=post.date)
                    daily_result.num -=1
                    if daily_result.num <= 0:
                        daily_result.delete()
                    else:
                        if post.winlose == 'WIN':
                            daily_result.win_ratio = round((Post.objects.filter(date=post.date, user=post.user, winlose='WIN').count() - 1) * 100 / daily_result.num, 1)
                        
                        if post.AP == 'AP':
                            daily_result.ap_ratio = round((Post.objects.filter(date=post.date, user=post.user, AP='AP').count() - 1) * 100 / daily_result.num, 1)
                        daily_result.save()

                    #楽曲ごと
                    song_result = SongResult.objects.get(user=post.user, title=post.title)
                    song_result.num -=1
                    if song_result.num <= 0:
                        song_result.delete()
                    else:
                        if post.winlose == 'WIN':
                            song_result.win_ratio = round((Post.objects.filter(title=post.title, user=post.user, winlose='WIN').count() - 1) * 100 / song_result.num, 1)
                        
                        if post.AP == 'AP':
                            song_result.ap_ratio = round((Post.objects.filter(title=post.title, user=post.user, AP='AP').count() - 1) * 100 / song_result.num, 1)
                        song_result.save()

                except Post.DoesNotExist:
                    pass

            # レコードを一括削除
            Post.objects.filter(pk__in=selected_ids).delete()
            
        return redirect(reverse('orc:post_list'))

class PostCreateFormView(LoginRequiredMixin, generic.FormView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    template_name = "orc/post_form.html"
    form_class = PostCreateForm
    success_url = reverse_lazy('orc:post_list')

    def form_valid(self, form):

        for image in self.request.FILES.getlist('images'):
            # 画像を新しいPostモデルのインスタンスとして保存する
            post = Post()
            results = recognition.rec(image)
            if len(results) != 8:
                continue
            post.title = results[0]
            post.winlose = results[1]
            post.perfect = results[2]
            post.great = results[3]
            post.good = results[4]
            post.bad = results[5]
            post.miss = results[6]
            post.AP = results[7]
            post.image = image
            post.user = self.request.user
            post.date = form.cleaned_data['date']
            post.save()

        return super().form_valid(form)

class PostDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = Post  # pk(primary key)はurls.pyで指定しているのでここではmodelを呼び出すだけで済む

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(self.model, pk=pk)

class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = Post
    form_class = PostCreateForm # PostCreateFormをほぼそのまま活用できる
    success_url = reverse_lazy('orc:post_detail')