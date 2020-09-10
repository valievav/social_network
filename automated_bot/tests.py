import logging
import unittest
from unittest.mock import patch

from automated_bot.auto_bot import AutomatedBot


class TestAutomatedBot(unittest.TestCase):

    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

        self.username = f'user'
        self.email = f'user@gmail.com'
        self.password = '12345'
        self.access_token = 'access'
        self.post_title = f"{self.username}'s test post"
        self.post_body = f"Test post content."
        self.post_id = 1

        self.base_url = 'http://127.0.0.1:8000/api/'
        self.register_url = f'{self.base_url}user/register/'
        self.login_url = f'{self.base_url}user/token/'
        self.post_url = f'{self.base_url}posts/'
        self.post_like_url = f'{self.base_url}posts/post_id/like/'

        self.bot = AutomatedBot(self.username, self.email, self.password,
                                self.base_url, self.register_url, self.login_url, self.post_url, self.post_like_url)


    @patch('automated_bot.auto_bot.requests.post')
    def test_register_success(self, mocked_post):
        mocked_post.return_value.status_code = 201
        result = self.bot.register()
        self.assertEqual(result, True)

    @patch('automated_bot.auto_bot.requests.post')
    def test_register_fail(self, mocked_post):
        mocked_post.return_value.status_code = 400
        result = self.bot.register()
        self.assertEqual(result, False)

    @patch('automated_bot.auto_bot.requests.post')
    def test_login_success(self, mocked_post):
        mocked_post.return_value.status_code = 200
        mocked_post.return_value.json.return_value = {'access': '123', 'refresh': '123'}
        result = self.bot.login()
        self.assertEqual(result, ('123', '123'))

    @patch('automated_bot.auto_bot.requests.post')
    def test_login_fail(self, mocked_post):
        mocked_post.return_value.status_code = 400
        result = self.bot.login()
        self.assertEqual(result, (None, None))

    @patch('automated_bot.auto_bot.requests.post')
    def test_post_success(self, mocked_post):
        mocked_post.return_value.status_code = 201
        result = self.bot.post(self.access_token, self.post_title, self.post_body)
        self.assertEqual(result, True)

    @patch('automated_bot.auto_bot.requests.post')
    def test_post_fail(self, mocked_post):
        mocked_post.return_value.status_code = 400
        result = self.bot.post(self.access_token, self.post_title, self.post_body)
        self.assertEqual(result, False)

    @patch('automated_bot.auto_bot.requests.get')
    def test_get_all_posts_ids_success(self, mocked_get):
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {"results": [{"id": 109,
                                                                  "url": "http://127.0.0.1:8000/api/posts/109/"},
                                                                 {"id": 108,
                                                                  "url": "http://127.0.0.1:8000/api/posts/108/"}]}
        result = self.bot.get_all_posts_ids(self.access_token)
        self.assertEqual(result, [109, 108])

    @patch('automated_bot.auto_bot.requests.get')
    def test_get_all_posts_ids_fail(self, mocked_get):
        mocked_get.return_value.status_code = 400
        result = self.bot.get_all_posts_ids(self.access_token)
        self.assertEqual(result, None)

    @patch('automated_bot.auto_bot.requests.post')
    def test_post_like_success(self, mocked_post):
        mocked_post.return_value.status_code = 201
        result = self.bot.post_like(self.access_token, self.post_id)
        self.assertEqual(result, True)

    @patch('automated_bot.auto_bot.requests.post')
    def test_post_like_fail(self, mocked_post):
        mocked_post.return_value.status_code = 400
        result = self.bot.post_like(self.access_token, self.post_id)
        self.assertEqual(result, False)
