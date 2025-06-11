from django.contrib import admin
from .models import Movie, TopMovie, NowPlaying, Booking , Showtime , Hall

# Register your models here.
admin.site.register(Movie)
admin.site.register(TopMovie)
admin.site.register(NowPlaying)
admin.site.register(Booking)
admin.site.register(Showtime)
admin.site.register(Hall)
