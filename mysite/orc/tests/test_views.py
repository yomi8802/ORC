from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import os

from ..models import Post,CustomUser,SongResult,DailyResult

class PostIndexTests(TestCase):
    def setUp(self):
        image_content = b'binary image data'
        self.image = SimpleUploadedFile("image.jpg", image_content, content_type="image/jpeg")
        self.user = CustomUser.objects.create_user(username='testuser',password='testpassword')
        self.client = Client()
        post1 = Post.objects.create(
            title = 'test_title1',
            winlose = 'WIN',
            perfect = '1000',
            great = '0000',
            good = '0000',
            bad = '0000',
            miss = '0000',
            AP = '',
            date = '2002-08-08',
            image = self.image,
            user = self.user
            )
        post2 = Post.objects.create(
            title = 'test_title2',
            winlose = 'WIN',
            perfect = '1000',
            great = '0000',
            good = '0000',
            bad = '0000',
            miss = '0000',
            AP = '',
            date = '2002-08-08',
            image = self.image,
            user = self.user
            )
    def test_get(self):
        """ログインせずGET メソッドでアクセスしてステータスコード302を返されることを確認"""
        response = self.client.get(reverse('orc:index'))
        self.assertEqual(response.status_code, 302)
    def test_login_get(self):
        """ログイン後GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('orc:index'))
        self.assertEqual(response.status_code, 200)
    def tearDown(self):
        """
        setUp で追加したデータを消す、掃除用メソッド。
        create とはなっているがメソッド名を「tearDown」とすることで setUp と逆の処理を行ってくれる＝消してくれる。
        """
        post1 = Post.objects.create(
            title = 'test_title1',
            winlose = 'WIN',
            perfect = '1000',
            great = '0000',
            good = '0000',
            bad = '0000',
            miss = '0000',
            AP = '',
            date = '2002-08-08',
            image = self.image,
            user = self.user
            )
        post2 = Post.objects.create(
            title = 'test_title2',
            winlose = 'WIN',
            perfect = '1000',
            great = '0000',
            good = '0000',
            bad = '0000',
            miss = '0000',
            AP = '',
            date = '2002-08-08',
            image = self.image,
            user = self.user
            )
        self.image.close()


class PostListTests(TestCase):
    def setUp(self):
        """
        テスト環境の準備用メソッド。名前は必ず「setUp」とすること。
        同じテストクラス内で共通で使いたいデータがある場合にここで作成する。
        """
        image_content = b'binary image data'
        self.image = SimpleUploadedFile("image.jpg", image_content, content_type="image/jpeg")
        self.user = CustomUser.objects.create_user(username='testuser',password='testpassword')
        self.client = Client()
        post1 = Post.objects.create(
            title = 'test_title1',
            winlose = 'WIN',
            perfect = '1000',
            great = '0000',
            good = '0000',
            bad = '0000',
            miss = '0000',
            AP = '',
            date = '2002-08-08',
            image = self.image,
            user = self.user
            )
        post2 = Post.objects.create(
            title = 'test_title2',
            winlose = 'WIN',
            perfect = '1000',
            great = '0000',
            good = '0000',
            bad = '0000',
            miss = '0000',
            AP = '',
            date = '2002-08-08',
            image = self.image,
            user = self.user
            )

    def test_get(self):
        """ログインせずGET メソッドでアクセスしてステータスコード302を返されることを確認"""
        response = self.client.get(reverse('orc:post_list'))
        self.assertEqual(response.status_code, 302)
    
    def test_login_get(self):
        """ログイン後GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('orc:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_get_2posts_by_list(self):
        """GET でアクセス時に、setUp メソッドで追加した 2件追加が返されることを確認"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('orc:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            # Postモデルでは __str__ の結果としてタイトルを返す設定なので、返されるタイトルが投稿通りになっているかを確認
            response.context['post_list'],
            ['<Post: test_title1>', '<Post: test_title2>'],
            ordered = False # 順序は無視するよう指定
        )
        self.assertContains(response, 'test_title1') # html 内に post1 の title が含まれていることを確認
        self.assertContains(response, 'test_title2') # html 内に post2 の title が含まれていることを確認

    def tearDown(self):
        """
        setUp で追加したデータを消す、掃除用メソッド。
        create とはなっているがメソッド名を「tearDown」とすることで setUp と逆の処理を行ってくれる＝消してくれる。
        """
        post1 = Post.objects.create(
            title = 'test_title1',
            winlose = 'WIN',
            perfect = '1000',
            great = '0000',
            good = '0000',
            bad = '0000',
            miss = '0000',
            AP = '',
            date = '2002-08-08',
            image = self.image,
            user = self.user
            )
        post2 = Post.objects.create(
            title = 'test_title2',
            winlose = 'WIN',
            perfect = '1000',
            great = '0000',
            good = '0000',
            bad = '0000',
            miss = '0000',
            AP = '',
            date = '2002-08-08',
            image = self.image,
            user = self.user
            )
        self.image.close()

class PostCreateTests(TestCase):
    """PostCreateビューのテストクラス."""

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser',password='testpassword')
        self.client = Client()
        image_path = '../mysite/media/img/IMG_5404.png'
        with open(image_path, 'rb') as image_file:
            self.image = SimpleUploadedFile(image_path, image_file.read(), content_type='image/png')
        image_path = '../mysite/media/img/test.png'
        with open(image_path, 'rb') as image_file:
            self.image2 = SimpleUploadedFile(image_path, image_file.read(), content_type='image/png')

    def test_get(self):
        """GET メソッドでアクセスしてステータスコード200を返されることを確認"""
        response = self.client.get(reverse('orc:post_form'))
        self.assertEqual(response.status_code, 302)
    
    def test_login_get(self):
        """ログイン後GETメソッドでアクセスしてステータスコード200を返されることを確認"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('orc:post_form'))
        self.assertEqual(response.status_code, 200)
    
    def test_post_with_data(self):
        """適当な画像でPOST すると、成功してリダイレクトされPostが作られることを確認"""
        self.client.login(username='testuser', password='testpassword')

        valid_date = timezone.now().date()

        response = self.client.post(reverse('orc:post_form'), {'images' : [self.image],'date' : valid_date,})

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(SongResult.objects.count(), 1)
        
        saved_posts = SongResult.objects.all()
        actual_post = saved_posts[0]

        self.assertEqual(actual_post.title, "トラッシュ・アンド・トラッシュ！")

        saved_posts = DailyResult.objects.all()
        actual_post = saved_posts[0]

        self.assertEqual(actual_post.date, valid_date)

    def test_post_with_ng_data(self):
        """不当な画像でPOST すると、成功してリダイレクトされるがPostが作られないことを確認"""
        self.client.login(username='testuser', password='testpassword')

        valid_date = timezone.now().date()

        response = self.client.post(reverse('orc:post_form'), {'images' : [self.image2],'date' : valid_date,})
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
    
    def test_post_null(self):
        """空のデータで POST を行うとリダイレクトも無く 200 だけ返されることを確認"""
        self.client.login(username='testuser', password='testpassword')
        data = {}
        response = self.client.post(reverse('orc:post_form'), data=data)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.image.close()

class PostDetailTests(TestCase):
    """PostDetailView のテストクラス"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser',password='testpassword')
        self.client = Client()
        image_content = b'binary image data'
        self.image = SimpleUploadedFile("image.jpg", image_content, content_type="image/jpeg")

    def test_not_fount_pk_get(self):
        """ログインしていない状態で記事を登録せず、空の状態で存在しない記事のプライマリキーでアクセスした時に 302 が返されることを確認"""
        response = self.client.get(
            reverse('orc:post_detail', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, 302)

    def test_login_not_fount_pk_get(self):
        """ログイン状態で記事を登録せず、空の状態で存在しない記事のプライマリキーでアクセスした時に 404 が返されることを確認"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('orc:post_detail', kwargs={'pk': 1}),
        )
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        """ログインせずGET メソッドでアクセスしてステータスコード302を返されることを確認"""
        post = Post.objects.create(
            title = 'test_title',
            winlose = 'WIN',
            perfect = '1000',
            great = '0000',
            good = '0000',
            bad = '0000',
            miss = '0000',
            AP = '',
            date = '2002-08-08',
            image = self.image,
            user = self.user,
            )
        response = self.client.get(
            reverse('orc:post_detail', kwargs={'pk': post.pk}),
        )
        self.assertEqual(response.status_code, 302)

    def test_login_get(self):
        """ログインしてGET メソッドでアクセスしてステータスコード200を返されることを確認"""
        self.client.login(username='testuser', password='testpassword')
        post = Post.objects.create(
            title = 'test_title',
            winlose = 'WIN',
            perfect = '1000',
            great = '0000',
            good = '0000',
            bad = '0000',
            miss = '0000',
            AP = '',
            date = '2002-08-08',
            image = self.image,
            user = self.user,
            )
        response = self.client.get(
            reverse('orc:post_detail', kwargs={'pk': post.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title)
        self.assertContains(response, post.perfect)
        self.assertContains(response, post.great)
        self.assertContains(response, post.good)
        self.assertContains(response, post.bad)
        self.assertContains(response, post.miss)
        self.assertContains(response, post.AP)
        self.assertContains(response, post.date)

    def tearDown(self):
        self.image.close()