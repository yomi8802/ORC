from django import forms
from .models import Post
from django.utils import timezone

class PostCreateForm(forms.ModelForm): # DjangoのModelFormでは強力なValidationを使える

    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'id': 'imageInput'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=timezone.now().date(), input_formats=['%Y-%m-%d'])

    class Meta:
        model = Post # Post モデルと接続し、Post モデルの内容に応じてformを作ってくれる
        fields = ['images','date']# 入力するカラムを指定

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user = user
            self.fields['user'] = forms.CharField(widget=forms.HiddenInput(),initial=user)

class PostBulkDeleteForm(forms.Form):
    selected_ids = forms.ModelMultipleChoiceField(
        queryset=Post.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )