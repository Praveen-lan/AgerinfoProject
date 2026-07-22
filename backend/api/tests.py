from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import News, Gallery, Slider, Topic


class PublicAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_counts_endpoint(self):
        response = self.client.get('/api/counts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('news', response.data)
        self.assertIn('gallery', response.data)
        self.assertIn('slider', response.data)
        self.assertIn('topics', response.data)

    def test_news_list(self):
        response = self.client.get('/api/news/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_gallery_list(self):
        response = self.client.get('/api/gallery/')
        self.assertEqual(response.status_code, 200)

    def test_slider_list(self):
        response = self.client.get('/api/slider/')
        self.assertEqual(response.status_code, 200)

    def test_topics_list(self):
        response = self.client.get('/api/topics/')
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_create_denied(self):
        response = self.client.post('/api/news/create/', {'title': 'Test', 'content': 'Content'})
        self.assertIn(response.status_code, [401, 403])


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin@agerinfo.com',
            email='admin@agerinfo.com',
            password='testpass123'
        )

    def test_login_success(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'admin@agerinfo.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_wrong_password(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'admin@agerinfo.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 401)

    def test_login_missing_fields(self):
        response = self.client.post('/api/auth/login/', {'email': ''})
        self.assertEqual(response.status_code, 400)


class AuthenticatedAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin@agerinfo.com',
            email='admin@agerinfo.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_news(self):
        response = self.client.post('/api/news/create/', {
            'title': 'Test News',
            'content': 'Test content',
            'category': 'general'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(News.objects.count(), 1)

    def test_create_gallery(self):
        response = self.client.post('/api/gallery/create/', {
            'title': 'Test Photo',
            'description': 'A test photo'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Gallery.objects.count(), 1)

    def test_create_slider(self):
        response = self.client.post('/api/slider/create/', {
            'image': 'https://example.com/img.jpg',
            'caption': 'Test slide'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Slider.objects.count(), 1)

    def test_create_topic(self):
        response = self.client.post('/api/topics/create/', {
            'title': 'Test Topic',
            'description': 'A test topic',
            'link': 'https://example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Topic.objects.count(), 1)

    def test_update_news(self):
        news = News.objects.create(title='Old', content='Old content')
        response = self.client.patch(f'/api/news/{news.id}/update/', {'title': 'New'})
        self.assertEqual(response.status_code, 200)
        news.refresh_from_db()
        self.assertEqual(news.title, 'New')

    def test_delete_news(self):
        news = News.objects.create(title='To Delete', content='Delete me')
        response = self.client.delete(f'/api/news/{news.id}/delete/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(News.objects.count(), 0)

    def test_update_slider(self):
        slider = Slider.objects.create(image='https://example.com/old.jpg')
        response = self.client.patch(f'/api/slider/{slider.id}/update/', {'caption': 'Updated'})
        self.assertEqual(response.status_code, 200)
        slider.refresh_from_db()
        self.assertEqual(slider.caption, 'Updated')

    def test_delete_requires_auth(self):
        unauth_client = APIClient()
        news = News.objects.create(title=' Protected', content='Content')
        response = unauth_client.delete(f'/api/news/{news.id}/delete/')
        self.assertIn(response.status_code, [401, 403])
