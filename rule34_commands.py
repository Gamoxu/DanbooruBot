from __future__ import unicode_literals
from rule34Py import rule34Py

r34Py = rule34Py()


def r34get_post_info(checkpost):
  post_info = [checkpost.image, checkpost.owner, "https://rule34.xxx/index.php?page=post&s=view&id=" + str(checkpost.id), checkpost.score]
  return post_info

def r34search_tags(usertags: str):
  posts = r34Py.search([usertags], limit=100)
  for post in posts:
    return post


def r34get_posts(usertags: str):
  posts = r34Py.search([usertags], limit=100)
  return posts
