import elasticsearch

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Video, APIKey
from .serializers import VideoSerializer
from .documents import VideoDocument
from .tasks import *


class GetVideoDetails(APIView):
    """
    Home Page API for the App - Displays latest results.

    """

    def get(self, request):
        paginator = PageNumberPagination()
        videos = Video.objects.all()
        paginated_videos = paginator.paginate_queryset(videos, request)
        serialized_videos = VideoSerializer(paginated_videos, many=True)

        return Response(status=status.HTTP_200_OK, data={"message": "Success", "data": serialized_videos.data})


class SearchVideo(APIView):
    """
    Search API - Displays results based on some keyword search, Uses Elastic Search

    """

    def get(self, request):
        paginator = PageNumberPagination()
        title_query = request.GET.get("title_query", None)
        description_query = request.GET.get("description_query", None)

        try:
            videos = VideoDocument.search()
            if title_query:
                videos = videos.query("match", title=title_query)
            if description_query:
                videos = videos.query("match", description=description_query)
            response = videos.execute()
            paginated_videos = paginator.paginate_queryset(response, request)
            serialized_videos = VideoSerializer(paginated_videos, many=True)

            return Response(status=status.HTTP_200_OK, data={"message": "Success", "data": serialized_videos.data})
        except AttributeError:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED, data={"message": "Empty Database"})
        except:
            es_create_index_if_not_exists(elasticsearch, "video")


class AddAPIKeys(APIView):
    """
    Add API Keys API - Can be used to add multiple APIKeys

    """

    def post(self, request):
        keys = request.data.get("keys", [])

        for key in keys:
            try:
                apikey = APIKey.objects.get(key=key)
            except:
                apikey = APIKey(
                    key=key
                )
                apikey.save()

        return Response(status=status.HTTP_200_OK, data={"message": "Success - API Keys Added Successfully"})
