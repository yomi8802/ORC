from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm): # DjangoのModelFormでは強力なValidationを使える

    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Post # Post モデルと接続し、Post モデルの内容に応じてformを作ってくれる
        fields = ['images'] # 入力するカラムを指定