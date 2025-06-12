from litellm import completion
from django.conf import settings
from django.http import HttpRequest, JsonResponse

from hacker_news.models import Story


def summarize_story(request: HttpRequest, story_id: int) -> JsonResponse:
  story = Story.objects.prefetch_related('articles').get(id=story_id)
  article = story.articles.first()

  if not article:
    return JsonResponse({"error": "No article found for this story"}, status=404)

  content = f"""Analyze the following news article and summarize it in a few sentences.
    Title: {story.title}

    Text: {story.text}

    Article: {article.text}
    """
  response = completion(
    model="ollama/mistral",
    messages=[
      {"role": "user", "content": content}
    ],
    api_base=settings.OLLAMA_API_BASE
  )
  return JsonResponse({"summary": response.choices[0].message.content})
