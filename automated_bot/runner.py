import os
import random
import time
from configparser import ConfigParser
from typing import Dict

from automated_bot.auto_bot import AutomatedBot
from automated_bot.logger import logger


def bot_runner(number_of_users: int, max_posts_per_user: int, max_likes_per_user: int,
               base_url: str, api_urls: Dict) -> None:

    # run bot for users
    for user_num in range(number_of_users):
        posts_per_user = random.randint(0, max_posts_per_user)
        likes_per_user = random.randint(0, max_likes_per_user)

        # user template data
        username = f'user{user_num}'
        email = f'user{user_num}@gmail.com'
        password = '12345'
        post_title = f"{username}'s adventure"
        post_body = f"Hey, my name is {username} and here's my adventure story on the great desert planet."

        bot = AutomatedBot(username, email, password, base_url, **api_urls)

        # register 1st time users, for existing will return 400
        bot.register()

        access_token, refresh_token = bot.login()
        if not all((access_token, refresh_token)):
            return

        # each user creates random number of posts
        logger.debug(f'>>> User {username} about to create {posts_per_user} posts.')
        for post_run in range(posts_per_user):
            if not bot.post(access_token, post_title, post_body):
                continue
            logger.debug(f'Created post with title {post_title}.')

        # posts are liked randomly, posts can be liked multiple times
        logger.debug(f'>>> User {username} about to give {likes_per_user} likes.')
        for like_run in range(likes_per_user):
            all_ids = bot.get_all_posts_ids(access_token)
            # break if no posts to like
            if not all_ids:
                break
            id_to_like = random.choice(all_ids)
            # move to next post_id if current like cannot be completed
            if not bot.post_like(access_token, id_to_like):
                continue
            logger.debug(f'Liked post with id {id_to_like}.')


if __name__ == '__main__':
    # bot config
    parser = ConfigParser()
    cwd = os.path.dirname(os.path.abspath(__file__))
    parser.read(os.path.join(cwd, 'config.ini'))
    number_of_users = parser.getint('bot', 'number_of_users')
    max_posts_per_user = parser.getint('bot', 'max_posts_per_user')
    max_likes_per_user = parser.getint('bot', 'max_likes_per_user')

    # API urls
    base_url = 'http://127.0.0.1:8000/api/'
    api_urls = {'register_url': f'{base_url}user/register/',
                'login_url': f'{base_url}user/token/',
                'post_url': f'{base_url}posts/',
                'post_like_url': f'{base_url}posts/post_id/like/'}

    logger.debug('Process started.')
    start = time.time()

    bot_runner(number_of_users, max_posts_per_user, max_likes_per_user, base_url, api_urls)

    time_elapsed = time.time() - start
    logger.debug(f'Process finished in {time.strftime("%H:%M:%S", time.gmtime(time_elapsed))}')
