from typing import Tuple, List, Optional

import requests

from automated_bot.logger import logger


class AutomatedBot:
    def __init__(self, username: str, email: str, password: str,
                 base_url: str, register_url: str, login_url: str, post_url: str, post_like_url: str):
        self.username = username
        self.email = email
        self.password = password

        self.base_url = base_url
        self.register_url = register_url
        self.login_url = login_url
        self.post_url = post_url
        self.post_like_url = post_like_url

    def register(self) -> bool:
        """
        Register user.
        """
        payload = {'username': self.username, 'email': self.email, 'password': self.password, 'password2': self.password}
        response = requests.post(self.register_url, data=payload)

        if response.status_code == 201:
            return True
        else:
            logger.error(f'Issue during registration: {response.status_code, response.text}.')
            return False

    def login(self) -> Tuple:
        """
        Login user.
        Returned access and refresh tokens.
        """
        payload = {'username': self.username, 'password': self.password}
        response = requests.post(self.login_url, data=payload)

        if response.status_code == 200:
            return response.json()['access'], response.json()['refresh']
        else:
            logger.critical(f'Issue during login: {response.status_code, response.text}.')
            return None, None

    def post(self, access_token: str, post_title: str, post_body: str) -> bool:
        """
        Create post.
        """
        payload = {'title': post_title, 'body': post_body}
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(self.post_url, data=payload, headers=headers)

        if response.status_code == 201:
            return True
        else:
            logger.error(f'Issue during post creation: {response.status_code, response.text}.')
            return False

    def get_all_posts_ids(self, access_token: str) -> Optional[List]:
        """
        Get ids for all available posts.
        """
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.post_url, headers=headers)

        data = response.json()['results']
        if response.status_code == 200:
            return [data[i]['id'] for i in range(len(data))] if data else None
        else:
            logger.error(f'Issue during getting ids for all post: {response.status_code, response.text}.')
            return None

    def post_like(self, access_token, post_id) -> bool:
        """
        Like post.
        """
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(self.post_like_url.replace('post_id', str(post_id)), headers=headers)

        if response.status_code == 201:
            return True
        else:
            logger.error(f'Issue during liking post: {response.status_code, response.text}.')
            return False
