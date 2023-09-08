from __future__ import unicode_literals
from pybooru import Danbooru
from pybooru import api_danbooru



client = Danbooru('danbooru')

def get_post_info(checkpost):
  post_info = [checkpost['file_url'], checkpost['tag_string_artist'], checkpost['source'], checkpost['tag_string_character']]
  return post_info


def search_tags(usertags: str, random):
  posts = client.post_list(tags=usertags, limit=1, random=random)
  for post in posts:
    return post


def get_posts(usertags: str, random):
  posts = client.post_list(tags=usertags, limit = 100, random=random)
  postlist = []
  for post in posts:
    postlist.append(post)
  return postlist
