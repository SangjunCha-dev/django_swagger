from rest_framework import serializers

from .models import Musics, PlayList


class MusicSerializer(serializers.ModelSerializer):
    def validate(self, data: dict):
        return data

    class Meta:
        model = Musics
        fields = '__all__'  # 모든 필드 사용
        # fields = ('id', 'created_at', 'title', 'category', 'star_rating',)  # 응답 필드 지정

class MusicBodySerializer(serializers.Serializer):
    singer = serializers.CharField(help_text="가수명")
    title = serializers.CharField(help_text="곡 제목")
    category = serializers.ChoiceField(help_text="곡 범주", choices=('KPOP', 'POP', 'CLASSIC', 'ETC'))
    star_rating = serializers.ChoiceField(help_text="1~3 이내 지정 가능. 숫자가 클수록 좋아하는 곡", choices=(1, 2, 3), required=False)

class MusicQuerySerializer(serializers.Serializer):
    title = serializers.CharField(help_text="곡 제목으로 검색", required=False)
    star_rating = serializers.ChoiceField(help_text="곡 선호도로 검색", choices=(1, 2, 3), required=False)
    singer = serializers.CharField(help_text="가수명으로 검색", required=True)
    category = serializers.ChoiceField(help_text="카테고리로 검색", choices=('KPOP', 'POP', 'CLASSIC', 'ETC'), required=False)
    created_at = serializers.DateTimeField(help_text="입력한 날짜를 기준으로 그 이전에 추가된 곡들을 검색", required=False)

class MusicForPlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musics
        fields = ('singer', 'title', 'category', 'star_rating',)
        
class PlayListSerializer(serializers.ModelSerializer):
    music = MusicForPlayListSerializer(read_only=True)
    # music = MusicSerializer(read_only=True)  # Music 모든 필드 조회

    class Meta:
        model = PlayList
        fields = ('playlist_name', 'created_at', 'updated_at','music',)

class PlayListQuerySerializer(serializers.Serializer):
    title = serializers.CharField(help_text="곡 제목 검색", required=False)
    singer = serializers.CharField(help_text="가수 이름 검색", required=False)
    
class PlayListBodySerializer(serializers.Serializer):
    name = serializers.CharField(help_text="플레이 리스트 이름")
    playlist = MusicBodySerializer(read_only=True)
