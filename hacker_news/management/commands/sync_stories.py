from typing import Any, Dict
from django.core.management import BaseCommand

from hacker_news.services.hacker_news_api.service import HackerNewsApiService
from hacker_news.tasks.sync_item import sync_item


class Command(BaseCommand):
  help = "Sync stories from Hacker News API"

  def add_arguments(self, parser):
    parser.add_argument('--count', action='store', dest='count', default=50,
        help='Number of stories to sync')

  def handle(self, *args: Dict[str, Any], **options: Dict[str, Any]) -> None:
    count = int(options.get('count', 50))
    api_service = HackerNewsApiService()
    best_stories = api_service.get_best_stories()

    for story_id in best_stories[:count]:
      sync_item.delay(story_id)
