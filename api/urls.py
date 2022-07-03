from django.urls import path 

from .views import MusicListView, SearchMusicListView, MusicView, PlayListView, SearchPlayListView


urlpatterns = [ 
    path("music/", MusicListView.as_view(), name="musics"),
    path("music/search/", SearchMusicListView.as_view(), name="music_search"),
    path("music/<int:pk>/", MusicView.as_view(), name="music"),

    path("playlist/", PlayListView.as_view(), name="playlists"),
    path("playlist/<str:playlist_name>/", SearchPlayListView.as_view(), name="playlist"),
]
