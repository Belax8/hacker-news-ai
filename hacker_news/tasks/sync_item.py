from celery import shared_task
from datetime import timezone as dt_timezone
from django.utils import timezone

from hacker_news.tasks import sync_article
from hacker_news.models import User, Story, Comment
from hacker_news.services.hacker_news_api.service import HackerNewsApiService


@shared_task
def sync_item(item_id: int, story_id: int | None = None) -> None:
  api_service = HackerNewsApiService()
  item = api_service.get_item(item_id)
  if item['type'] == 'story':
    _sync_story(item)
  elif item['type'] == 'comment':
    _sync_comment(item, story_id)

def _get_or_create_user(username: str | None) -> User | None:
  if username is None:
    return None

  try:
    user = User.objects.filter(username=username).first()
    if user:
      return user
  except Exception:
    pass

  api_service = HackerNewsApiService()
  api_user = api_service.get_user(username)
  try:
    created_on = timezone.datetime.fromtimestamp(api_user['created'], tz=dt_timezone.utc) if api_user.get('created') else None
    user, _ = User.objects.update_or_create(
      username=api_user['id'],
      defaults={
        'karma': api_user.get('karma', 0),
        'created_on': created_on,
        'updated_on': timezone.now(),
      }
    )
  except Exception as e:
    user = None
  return user

def _sync_story(item: dict) -> None:
  user = _get_or_create_user(item.get('by', None))
  created_on = timezone.datetime.fromtimestamp(item['time'], tz=dt_timezone.utc) if item.get('time') else None

  story, _ = Story.objects.update_or_create(
    id=item['id'],
    defaults={
      'title': item.get('title', None),
      'text': item.get('text', None),
      'score': item.get('score', 0),
      'user': user,
      'url': item.get('url', None),
      'is_deleted': item.get('deleted', False),
      'created_on': created_on,
      'updated_on': timezone.now(),
    }
  )
  if story.url:
    sync_article.delay(story.id)

  for kid_id in item.get('kids', []):
    sync_item(kid_id, item['id'])

def _sync_comment(item: dict, story_id: int | None = None) -> None:
  user = _get_or_create_user(item.get('by', None))

  parent_id = None if story_id == item.get('parent', None) else item.get('parent', None)
  created_time = timezone.datetime.fromtimestamp(item['time'], tz=dt_timezone.utc) if item.get('time') else None

  Comment.objects.update_or_create(
    id=item['id'],
    defaults={
      'story_id': story_id,
      'parent_id': parent_id,
      'text': item.get('text', None),
      'user': user,
      'is_deleted': item.get('deleted', False),
      'created_on': created_time,
      'updated_on': timezone.now(),
    }
  )

  for kid_id in item.get('kids', []):
    sync_item(kid_id, story_id)
