"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist

class SongView(ViewSet):

    def retrieve(self, request, pk):
        try:
            song = Song.objects.prefetch_related('genres').get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        songs = Song.objects.all()

        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
    def create(self, request):
        artist_id = Artist.objects.get(pk=request.data["artist_id"])
        song = Song.objects.create(
            title = request.data["title"],
            album = request.data["album"],
            length = request.data["length"],
            artist_id=artist_id,
        )
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.album = request.data["album"]
        song.length = request.data["length"]
        song.artist_id = Artist.objects.get(pk=request.data["artist_id"])
        song.save()

        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class SongSerializer(serializers.ModelSerializer):
    artist = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Song
        fields = ('id', 'title', 'artist', 'album', 'length', 'genres')

    def get_genres(self, obj):
        genres = obj.genres.all()
        return [{'id': genre.genre_id.id, 'description': genre.genre_id.description} for genre in genres]

    def get_artist(self, obj):
        artist = obj.artist_id
        return {'id': artist.id, 'name': artist.name, 'age': artist.age, 'bio': artist.bio}
