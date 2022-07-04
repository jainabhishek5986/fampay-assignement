from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from youtube_api_integration.models import Video
from rest_framework.pagination import PageNumberPagination
from youtube_api_integration.serializers import VideoSerializer


class GetVideoDetails(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        page = request.GET.get("page", 1)
        videos = Video.objects.all()
        paginated_videos = paginator.paginate_queryset(videos, page)
        serialized_videos = VideoSerializer(paginated_videos, many=True)

        return Response(status=status.HTTP_200_OK, data={"message": "Success", "data": serialized_videos.data})

class SearchVideo(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        page = request.GET.get("page", 1)
        query = request.GET.get("query")
        videos = Video.objects.filter(title__contains=query)
        paginated_videos = paginator.paginate_queryset(videos, page)
        serialized_videos = VideoSerializer(paginated_videos, many=True)

        return Response(status=status.HTTP_200_OK, data={"message": "Success", "data": serialized_videos.data})