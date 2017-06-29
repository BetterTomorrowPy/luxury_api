from django.test import TestCase
from django.contrib.auth.models import User

from posts.models import *


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