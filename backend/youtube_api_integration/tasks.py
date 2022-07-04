import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from backend.settings import (
    API_SERVICE_NAME,
    API_VERSION,
)

def search(query, interval, max_results):
    from youtube_api_integration.models import APIKey
    api_keys = APIKey.objects.filter().all().values_list('key', flat=True)

    for key in api_keys:
        try:
            youtube = build(API_SERVICE_NAME, API_VERSION , key)
            published_after = (datetime.now - datetime.timedelta(minutes = interval)).isoformat + "Z"

            response = (
                youtube.search().list(
                    q = query,
                    part = "snippet",
                    type = "video",
                    maxResults = max_results,
                    order = "date",
                    publishedAfter = published_after
                ).execute()
            )
            return response
        except HttpError as err:
            print("An HTTP error %d occurred:\n%s" % (err.resp.status, err.content))
            if err.resp.status == 403:
                print(f"Request Failed with API_KEY_{num}")
                continue
            return dict()