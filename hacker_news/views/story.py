from django.shortcuts import render

from hacker_news.models import Story, Comment


def story(request, story_id: int):
  story = Story.objects.prefetch_related('articles').get(id=story_id)
  article = story.articles.first()
  comments = Comment.objects.select_related('user').filter(story_id=story_id)

  context = {
    'story': story,
    'article': article,
    'comments': _map_comments(comments)
  }
  return render(request, 'story.html', context)

def _map_comments(comments):
  """
  Maps comments with a nested `replies` field.
  These can be nested to any depth.
  Returns only top-level comments (those without parents), with nested replies.
  """
  # Create a mapping of parent_id to list of child comments
  comment_map = {}
  for comment in comments:
    parent_id = comment.parent_id
    if parent_id not in comment_map:
      comment_map[parent_id] = []
    comment_map[parent_id].append(comment)
    
  # Recursively attach replies to each comment
  def attach_replies(comment):
    # Preserve the comment object as is, just add the replies attribute
    comment.replies = comment_map.get(comment.id, [])
    for reply in comment.replies:
      attach_replies(reply)
    return comment
    
  # Get top-level comments (those with no parent) and attach their replies
  top_level_comments = comment_map.get(None, [])
  for comment in top_level_comments:
    attach_replies(comment)
    
  return top_level_comments
