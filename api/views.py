from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Musics, PlayList
from .serializers import MusicSerializer, MusicBodySerializer, MusicQuerySerializer, \
    PlayListSerializer, PlayListQuerySerializer, PlayListBodySerializer

music_list_response = openapi.Response('', MusicSerializer(many=True))


class MusicListView(APIView):
    @swagger_auto_schema(responses={200: music_list_response})
    def get(self, request):
        '''
        음악 목록 조회

        ---
        '''
        serializer = MusicSerializer(Musics.objects.all(), many=True)

        response = Response(data=serializer.data)
        return response

    @swagger_auto_schema(request_body=MusicBodySerializer)
    def post(self, request):
        '''
        음악 추가

        ---
        '''
        musics = Musics.objects.filter(**request.data)
        if musics.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = MusicSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        music = serializer.save()

        response = Response(data=MusicSerializer(music).data, status=status.HTTP_201_CREATED)
        return response


class SearchMusicListView(APIView):
    @swagger_auto_schema(query_serializer=MusicQuerySerializer)
    def get(self, request):
        '''
        음악 검색

        ---
        '''
        query_string = request.GET

        conditions = {
            'title__contains': query_string.get('title', None),
            'star_rating': query_string.get('star_rating', None),
            'singer__contains': query_string.get('singer', None),
            'category': query_string.get('category', None),
            'created_at__lte': query_string.get('created_at', None),
        }
        conditions = {
            key: val for key, val in conditions.items() if val is not None
        }

        musics = Musics.objects.filter(**conditions)
        serializer = MusicSerializer(musics, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response


class MusicView(APIView): 
    def get_object(self, pk):
        return get_object_or_404(Musics, pk=pk)

    def get(self, request, pk):
        '''
        음악 정보 조회

        ---
        '''
        serializer = MusicSerializer(Musics.objects.filter(id=pk), many=True)

        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response

    @swagger_auto_schema(
        request_body=MusicBodySerializer,       # Request Serializer 지정
        manual_parameters=[openapi.Parameter(
            name='header_test',                 # api 파라미터 이름
            in_=openapi.IN_HEADER,              # 파라미터 종류 (header = openapi.IN_HEADER)
            description="a header for test",    # 파라미터 설명
            type=openapi.TYPE_STRING            # header 지정시 필수 선언
        )],
    )
    def put(self, request, pk):
        '''
        음악 정보 수정

        ---
        '''
        object = self.get_object(pk=pk)
        serializer = MusicSerializer(object, data=request.data)

        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

        serializer.save()
        response = Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        return response

    def delete(self, request, pk):
        '''
        음악 정보 삭제

        ---
        '''
        object = self.get_object(pk=pk)
        object.delete()

        response = Response(status=status.HTTP_204_NO_CONTENT)
        return response


class PlayListView(APIView):
    @swagger_auto_schema(query_serializer=PlayListQuerySerializer)
    def get(self, request):
        '''
        재생 목록 조회

        ---
        '''
        query_string = request.GET

        conditions = {
            'music__title__contains': query_string.get('title', None),
            'music__singer__contains': query_string.get('singer', None),
        }
        conditions = {
            key: val for key, val in conditions.items() if val is not None
        }

        playlist = PlayList.objects.filter(**conditions)

        serializer = PlayListSerializer(playlist, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response

    @swagger_auto_schema(request_body=PlayListBodySerializer)
    def post(self, request):
        '''
        재생 목록 추가

        ---
        '''
        conditions = request.data.get('playlist')
        music = Musics.objects.get(**conditions)
        playlist = PlayList.objects.create(
            playlist_name=request.data.get('name'),
            music=music,  # model instance 또는 pk
        )
        playlist.save()

        response = Response(data=PlayListSerializer(playlist).data, status=status.HTTP_201_CREATED)
        return response


class SearchPlayListView(APIView):
    @swagger_auto_schema(query_serializer=PlayListQuerySerializer)
    def get(self, request, playlist_name):
        '''
        재생 목록 검색

        ---
        '''
        query_string = request.GET

        conditions = {
            'playlist_name': playlist_name,
            'music__title__contains': query_string.get('title', None),
            'music__singer__contains': query_string.get('singer', None),
        }
        conditions = {
            key: val for key, val in conditions.items() if val is not None
        }

        playlist = PlayList.objects.filter(**conditions)

        serializer = PlayListSerializer(playlist, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response
