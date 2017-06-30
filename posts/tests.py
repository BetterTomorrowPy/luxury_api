import json
import requests
from django.test import TestCase
from django.utils.http import urlencode

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
        print('get-body-> ', body)
        self.assertEqual(body.get('code'), 1000)
        requests.get()

    def test_post_label_create(self):
        u = User.objects.get(username=test_user['username'])
        data = {
            "user_id": u.id,
            "label_name": "育儿基金"
        }
        response = self.client.post('/posts/post_label/', data=json.dumps(data), content_type='application/json')
        body = response.json()
        print('body -> ', body)
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
        super(PostTestCase, cls).setUpClass()

    def test_post_create(self):
        u = User.objects.get(username='guppy')
        params = {
            'user': u,
            'followers': None,
            # 'label': None,
            'post_type': 3,
            'post_title': '测试卡片',
            'post_content': 'XXXXXXXXXXXXXXXX'
        }
        p = Post.objects.create(**params)
        self.assertEqual(p.post_title, '测试卡片')
        self.assertEqual(p.is_deleted, 0)