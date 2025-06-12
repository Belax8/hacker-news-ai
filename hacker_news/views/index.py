from django.shortcuts import render
from django.db.models import Count

from hacker_news.models import Story

def index(request):
    stories = Story.objects.filter(is_deleted=False).annotate(comment_count=Count('comments')).order_by('-created_on')[:50]

    context = {
        'stories': stories,
    }
    return render(request, 'index.html', context)
