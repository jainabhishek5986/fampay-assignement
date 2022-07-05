from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import elasticsearch

from backend.settings import (
    API_SERVICE_NAME,
    API_VERSION,
)

"""Function to fetch the data from Youtube API - Used by Celery Task"""
def search(query, interval, max_results):
    from youtube_api_integration.models import APIKey
    api_keys = APIKey.objects.filter(is_limit_over=False)

    for key in api_keys:
        try:
            youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=key.key)
            published_after = (datetime.now() - timedelta(minutes=interval)).isoformat() + "Z"

            response = (
                youtube.search().list(
                    q=query,
                    part="snippet",
                    type="video",
                    maxResults=max_results,
                    order="date",
                    publishedAfter=published_after
                ).execute()
            )
            return response
        except HttpError as err:
            print("Response Code : " + str(err.resp.status) + ", Error : " + str(err))
            if err.resp.status == 403:
                print("Request Failed with API KEY : " + key.key)
                key.is_limit_over = True  #Key Usage limit Over
                key.save()
                print("Limit Updated for API KEY : " + key.key)
    return dict()


def es_create_index_if_not_exists(es, index):
    """Create the given ElasticSearch index and ignore error if it already exists"""
    try:
        es.indices.create(index)
    except elasticsearch.exceptions.RequestError as ex:
        if ex.error == 'resource_already_exists_exception':
            pass  # Index already exists. Ignore.
        else:  # Other exception - raise it
            raise ex
