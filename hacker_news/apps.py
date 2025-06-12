from django.apps import AppConfig


class HackerNewsConfig(AppConfig):
  name = "hacker_news"
  verbose_name = "Hacker News"
  default_site = "hacker_news.admin.HackerNewsSite"

  def ready(self) -> None:
    pass
