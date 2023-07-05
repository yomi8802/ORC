# Create your views here.
import os

from django.views import generic
from django.urls import reverse_lazy
from .forms import PostCreateForm # forms.py で作ったクラスをimport
from .models import Post

class PostListView(generic.ListView):
    model = Post

class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('orc:post_list')

    def form_valid(self, form):

        for image in self.request.FILES.getlist('images'):
            # 画像を新しいPostモデルのインスタンスとして保存する
            post = Post()
            post.title = form.cleaned_data['title']
            post.text = form.cleaned_data['text']
            post.image = image
            post.save()

        return super().form_valid(form)

class PostDetailView(generic.DetailView):
    model = Post  # pk(primary key)はurls.pyで指定しているのでここではmodelを呼び出すだけで済む

class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostCreateForm # PostCreateFormをほぼそのまま活用できる
    success_url = reverse_lazy('orc:post_detail')

class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('orc:post_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # 画像ファイルのパスを取得する処理を追加する
        image_path = self.object.image.path
        # レコードを削除する前に画像ファイルを削除する処理を追加する
        if os.path.exists(image_path):
            os.remove(image_path)
        return super().delete(request, *args, **kwargs)