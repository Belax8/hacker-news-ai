import requests


class HackerNewsApiService():
  """
  https://github.com/HackerNews/API
  """

  def __init__(self):
    self.base_url = "https://hacker-news.firebaseio.com/v0"

  def get_user(self, username: str) -> dict:
    response = requests.get(f"{self.base_url}/user/{username}.json")
    return response.json()

  def get_item(self, item_id: int) -> dict:
    response = requests.get(f"{self.base_url}/item/{item_id}.json")
    return response.json()

  def get_max_item_id(self) -> int:
    response = requests.get(f"{self.base_url}/maxitem.json")
    return response.json()

  def get_new_stories(self) -> list[int]:
    response = requests.get(f"{self.base_url}/newstories.json")
    return response.json()

  def get_best_stories(self) -> list[int]:
    response = requests.get(f"{self.base_url}/beststories.json")
    return response.json()