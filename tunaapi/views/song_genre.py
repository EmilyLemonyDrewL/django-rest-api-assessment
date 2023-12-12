from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre, Song, Genre

class SongGenreView(ViewSet):

    def create(self, request):
        song_id = request.data["song_id"]
        genre_id = request.data["genre_id"]

        # Retrieve the Song instance
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {"error": f"Song with id {song_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Retrieve the Genre instance
        try:
            genre = Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist:
            return Response(
                {"error": f"Genre with id {genre_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create the SongGenre instance
        song_genre = SongGenre.objects.create(
            song_id=song,
            genre_id=genre,
            )

        serializer = SongGenreSerializer(song_genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        """GET Single Song Genre"""
        song_genre = SongGenre.objects.get(pk=pk)
        serializer = SongGenreSerializer(song_genre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """GET All Song Genres"""
        songs = SongGenre.objects.all()
        serializer = SongGenreSerializer(songs, many=True)
        response_data = serializer.data
        print("SongGenreView response_data:", response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        """UPDATE Song Genre"""
        song_genre = SongGenre.objects.get(pk=pk)
        song_genre.song_id = Song.objects.get(pk=request.data["song_id"])
        song_genre.genre_id = Genre.objects.get(pk=request.data["genre_id"])
        song_genre.save()
        return Response('Song Genre updated', status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        """DELETE Song Genre"""
        song_genre = SongGenre.objects.get(pk=pk)
        song_genre.delete()
        return Response('Song Genre deleted', status=status.HTTP_204_NO_CONTENT)

class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for song genres"""
    class Meta:
        model = SongGenre
        fields = ('id', 'song_id', 'genre_id')
