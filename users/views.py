from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm,  ShowtimeSearchForm
from .models import *
from django.http import HttpResponse
from .management.commands import scrape, clear_lists


# Create your views here.
# Home page
def index(request):
    return render(request, 'index.html')

def now_playing_movies(request):
    now_playing_movies = NowPlaying.objects.all()
    return render(request, 'now_playing_movies.html', {'now_playing_movies': now_playing_movies})

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def showtime_search(request):
    if request.method == 'POST':
        form = ShowtimeSearchForm(request.POST)
        if form.is_valid():
            show_date = form.cleaned_data['date']  # Change 'date' to 'show_date'
            # Process the search based on the selected date
            showtimes = Showtime.objects.filter(show_date=show_date)  # Change 'date' to 'show_date'
            return render(request, 'showtime_search_results.html', {'showtimes': showtimes})
    else:
        form = ShowtimeSearchForm()
    return render(request, 'showtime_search.html', {'form': form})



# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

# other pages
def user_booked_movies(request):
    if request.user.is_authenticated:
        booked_movies = Booking.objects.filter(user=request.user)
        return render(request, 'my_booked_movies.html', {"booked_movies": booked_movies})
    else:
        return redirect('login')

def user_book_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        num_tickets = int(request.POST.get('num_tickets', 1))
        movie = Movie.objects.get(pk=movie_id)
        if movie:
            booking = Booking.objects.create(user=request.user, movie=movie, num_tickets=num_tickets)
            booking.save()
            return redirect('my_booked_movies')
    
    # Fetch movies that have corresponding entries in the Showtime model
    movies_list = Movie.objects.filter(showtime__isnull=False).distinct()
    return render(request, 'book_movie.html', {"movies_list": movies_list})


def ShowTopMovies(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        num_tickets = int(request.POST.get('num_tickets', 1))
        top_movie = TopMovie.objects.get(pk=movie_id)
        if top_movie:
            # Access the associated Movie instance
            movie = top_movie.movie
            booking = Booking.objects.create(user=request.user, movie=movie, num_tickets=num_tickets)
            booking.save()
            return redirect('my_booked_movies')
    
    top_movies_list = TopMovie.objects.all()  # Get all top movies
    return render(request, 'top_movies.html', {"top_movies_list": top_movies_list})

def book_movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'book_movie_detail.html', {"movie": movie})

def custom_admin_page(request):
    return render(request, 'admin/custom_admin_page.html')

def scrape_data_view(request):
    # Execute the 'scrape' management command
    scrape.Command().handle()
    return HttpResponse("Scraping data completed.")

def clear_lists_view(request):
    # Execute the 'clear_lists' management command
    clear_lists.Command().handle()
    return HttpResponse("Clearing lists completed.")
