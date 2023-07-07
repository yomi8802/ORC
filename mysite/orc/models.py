from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField('曲名', max_length=200)
    text = models.TextField('勝敗')
    date = models.DateTimeField('日付', default=timezone.now)
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.title