import json

from django.test import TestCase

from posts.models import *

test_user = {
    'username': 'test_user',
    'email': '13540471106@163.com',
    'password': 'bigbird'
}


class PostLabelTestCase(TestCase):
    """"""

    @classmethod
    def setUpClass(cls):
        u = User.objects.create_user(**test_user)
        super(PostLabelTestCase, cls).setUpClass()

    def test_get_labels(self):
        u = User.objects.get(username=test_user['username'])
        PostLabel.objects.create(user=u, label_name='开心一刻')
        params = {
            'page': 1,
            'per_size': 15
        }
        response = self.client.get('/posts/post_label/', data=params)
        body = response.json()
        self.assertEqual(body.get('code'), 1000)

    def test_post_label_create(self):
        u = User.objects.get(username=test_user['username'])
        data = {
            "user_id": u.id,
            "label_name": "育儿基金"
        }
        response = self.client.post('/posts/post_label/', data=json.dumps(data), content_type='application/json')
        body = response.json()
        self.assertEqual(body.get('code'), 1000)


class PostTestCase(TestCase):
    """"""

    @classmethod
    def setUpClass(cls):
        u = User.objects.create_user(
            username='guppy',
            email='2222@163.com',
            password='bigbird'
        )
        params = {
            'user': u,
            'post_type': 3,
            'post_title': '测试卡片',
            'post_content': 'XXXXXXXXXXXXXXXX'
        }
        Post.objects.create(**params)
        super(PostTestCase, cls).setUpClass()

    def test_get_post(self):
        response = self.client.get('/posts/posts/', data={'page': 1, 'per_size': 15})
        body = response.json()
        self.assertEqual(body.get('code'), 1000)

    def test_create_post(self):
        params = {
            'label_ids': [],
            'images': [],
            'videos': [],
            'post_type': 3,
            'post_title': '测试卡片',
            'post_content': 'XXXXXXXXXXXXXXXX'
        }
        response = self.client.post('/posts/posts/', data=json.dumps(params), content_type='application/json')
        body = response.json()
        self.assertEqual(body.get('code'), 1000)