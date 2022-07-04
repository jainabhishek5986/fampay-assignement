import os
from celery import Celery
from django.conf import settings
from dateutil import parser
from celery.utils.log import get_task_logger

from youtube_api_integration.tasks import search
from backend.settings import (
    SEARCH_QUERY,
    INTERVAL,
    MAX_RESULTS,
    BASE_URL,
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

logger = get_task_logger(__name__)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(bind=True)
def fetch_and_update_db(self):
    from youtube_api_integration.models import Video
    response = search(SEARCH_QUERY, INTERVAL, MAX_RESULTS)
    logger.info("Videos fetched Succesfully")
    for item in response.get("items", []):
        try:
            video = Video.objects.get(video_url=BASE_URL + item["id"]["videoId"])
            logger.info("Video Already Exists")
            continue
        except:
            logger.info("Creating new Video Entry in DB")
            snippet = item["snippet"]
            video = Video(
                title=snippet["title"],
                description=snippet["description"],
                published_at=parser.parse(snippet["publishedAt"]),
                thumbnail_url=snippet["thumbnails"]["default"]["url"],
                video_url=BASE_URL + item["id"]["videoId"]
            )
            video.save()
