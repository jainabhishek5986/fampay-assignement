from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from youtube_api_integration.models import Video
from rest_framework.pagination import PageNumberPagination
from youtube_api_integration.serializers import VideoSerializer
from .documents import Video as VideoDocument
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections


class GetVideoDetails(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        page = request.GET.get("page", 1)
        videos = Video.objects.all()
        paginated_videos = paginator.paginate_queryset(videos, request)
        serialized_videos = VideoSerializer(paginated_videos, many=True)

        return Response(status=status.HTTP_200_OK, data={"message": "Success", "data": serialized_videos.data})


class SearchVideo(APIView):
    def get(self, request):

        client = Elasticsearch()
        paginator = PageNumberPagination()
        page = request.GET.get("page", 1)
        title_query = request.GET.get("title_query", None)
        description_query = request.GET.get("description_query", None)

        videos = VideoDocument.search()
        if title_query:
            videos = videos.query("match", title=title_query)
        if description_query:
            videos = videos.query("match", description=description_query)
        response = videos.execute()
        paginated_videos = paginator.paginate_queryset(response, request)
        serialized_videos = VideoSerializer(paginated_videos, many=True)

        return Response(status=status.HTTP_200_OK, data={"message": "Success", "data": serialized_videos.data})
