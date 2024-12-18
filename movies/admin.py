from django import forms
from django.contrib import admin
from .models import Movie, Genre

class MovieAdminForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        thumbnail_file = cleaned_data.get("thumbnail_file")
        thumbnail_url = cleaned_data.get("thumbnail_url")
        banner_url = cleaned_data.get("banner_url")

        if not thumbnail_file and not thumbnail_url:
            raise forms.ValidationError("You must provide either a thumbnail file or a thumbnail URL.")
        if thumbnail_file and thumbnail_url:
            raise forms.ValidationError("You cannot provide both a thumbnail file and a thumbnail URL.")
        if banner_url and not banner_url:
            raise forms.ValidationError("Banner URL must be a valid URL starting with 'http'.")
        return cleaned_data

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm
    list_display = ('title', 'get_genres', 'rating', 'release_date')
    search_fields = ('title', 'genres__name')
    list_filter = ('genres', 'release_date')
    filter_horizontal = ('genres',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'genres', 'rating', 'thumbnail_file', 'thumbnail_url', 'banner_url', 'release_date')
        }),
        ('Watch and Trailer', {
            'fields': ('watch_link', 'trailer_link'),
            'description': '''
                <span style="font-size: 18px; font-weight: bold;">Watch Link</span><br>
                <span style="font-size: 16px; font-weight: bold;">If you are using google drive files make sure the format is like this --> https://drive.google.com/file/d/VIDEO_ID_HERE/preview</span><br>
                <span style="font-size: 16px; font-weight: bold;">If you are using VidSrc and TMDB make sure the format is like this --> https://vidsrc.me/embed/movie?tmdb=TMDB_ID_HERE</span><br>
                <span style="font-size: 16px; font-weight: bold;">If you are using VidSrc and IMDB make sure the format is like this --> https://vidsrc.me/embed/movie?imdb=IMDB_ID_HERE</span><br>
                <span style="font-size: 14px;">Below is the link to watch the movie. Please ensure the link is correct before saving.</span>
            '''
        }),
    )

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Genres'

admin.site.register(Genre)