from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField('曲名', max_length=200)
    winlose = models.TextField('勝敗')
    perfect = models.TextField('パーフェクト')
    great = models.TextField('グレート')
    good = models.TextField('グッド')
    bad = models.TextField('バッド')
    miss = models.TextField('ミス')
    date = models.DateTimeField('日付', default=timezone.now)
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        return self.title