from django.shortcuts import render, get_object_or_404
from .models import Movie, Genre
import random

def home(request):
    genres = Genre.objects.filter(movies__isnull=False).distinct()
    genre_movies = {
        genre: list(genre.movies.all().order_by('?')) for genre in genres
    }
    movies = list(Movie.objects.all())
    random_movies = random.sample(movies, 3) if len(movies) >= 3 else movies
    return render(request, 'movies/home.html', {
        'genres': genres,
        'genre_movies': genre_movies,
        'random_movies': random_movies
    })

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movies/detail.html', {'movie': movie})

def search_movies(request):
    query = request.GET.get('q', '')
    results = Movie.objects.filter(title__icontains=query) if query else None
    genres = Genre.objects.all()
    return render(request, 'movies/search_results.html', {
        'query': query,
        'results': results,
        'genres': genres,
    })

def search(request):
    query = request.GET.get('q', '')
    results = Movie.objects.filter(title__icontains=query) if query else []
    return render(request, 'movies/search_results.html', {'query': query, 'results': results})