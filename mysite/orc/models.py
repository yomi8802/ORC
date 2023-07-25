from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

#日付ごとの戦績を保存
class DailyResult(models.Model):
    date = models.DateField('日付')
    num = models.IntegerField('試合数', default=0)
    win_ratio = models.IntegerField('勝率', default=0)
    ap_ratio = models.IntegerField('AP率', default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#楽曲ごとの戦績を保存
class SongResult(models.Model):
    title = models.CharField('曲名', max_length=100)
    num = models.IntegerField('試合数', default=0)
    win_ratio = models.IntegerField('勝率', default=0)
    ap_ratio = models.IntegerField('AP率', default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#すべてのレコードを保存
class Post(models.Model):
    title = models.CharField('曲名', max_length=100)
    winlose = models.TextField('勝敗')
    perfect = models.TextField('perfect')
    great = models.TextField('great')
    good = models.TextField('good')
    bad = models.TextField('bad')
    miss = models.TextField('miss')
    AP = models.TextField('AP')
    date = models.DateField('日付')
    image = models.ImageField(upload_to='img/')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        #戦績を計算、保存
        #日付ごと
        daily_result, _ = DailyResult.objects.get_or_create(user=self.user, date=self.date)
        daily_result.num = Post.objects.filter(date=self.date, user=self.user).count()
        daily_result.win_ratio = round(Post.objects.filter(date=self.date, user=self.user, winlose='WIN').count() * 100 / daily_result.num, 1)
        daily_result.ap_ratio = round(Post.objects.filter(date=self.date, user=self.user, AP='AP').count() * 100 / daily_result.num, 1)
        daily_result.save()

        #楽曲ごと
        song_result, _ = SongResult.objects.get_or_create(user=self.user, title=self.title)
        song_result.num = Post.objects.filter(title=self.title, user=self.user).count()
        song_result.win_ratio = round(Post.objects.filter(title=self.title, user=self.user, winlose='WIN').count() * 100 / song_result.num, 1)
        song_result.ap_ratio = round(Post.objects.filter(title=self.title, user=self.user, AP='AP').count() * 100 / song_result.num, 1)
        song_result.save()