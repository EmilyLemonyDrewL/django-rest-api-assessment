from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, SongGenre

class GenreView(ViewSet):

    def retrieve(self, request, pk):
        try:
            genre = Genre.objects.prefetch_related('songs').get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        genres = Genre.objects.all()

        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        genre = Genre.objects.create(
          description=request.data["description"],
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

# create a custom genrealizer for songgenre
class SongGenreSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    artist_id = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()
    length = serializers.SerializerMethodField()

    class Meta:
        model = SongGenre
        fields = ('id', 'title', 'artist_id', 'album', 'length')

    def get_id(self, obj):
        return obj.song_id.id

    def get_title(self, obj):
        return obj.song_id.title

    def get_album(self, obj):
        return obj.song_id.album

    def get_length(self, obj):
        return obj.song_id.length

    def get_artist_id(self, obj):
        return obj.song_id.artist_id.id

class GenreSerializer(serializers.ModelSerializer):

    songs = SongGenreSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')
        depth = 1
