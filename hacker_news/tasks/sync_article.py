import requests
from celery import shared_task

from hacker_news.models import Story, Article


@shared_task
def sync_article(story_id: int):
  story = Story.objects.get(id=story_id)
  if story.url is None:
    return
  
  url = f'https://r.jina.ai/{story.url}'
  response = requests.get(url)
  if response.status_code != 200:
    raise Exception(f'Failed to sync article: {response.status_code}')

  Article.objects.create(story=story, text=response.text)
