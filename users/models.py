from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    original_title = models.CharField(max_length=500)
    released = models.DateField()
    poster = models.ImageField(upload_to='images')

    def __str__(self):
        return f"{self.original_title} ({self.released})"

class TopMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='top_movies')

    def __str__(self):
        return f"Top: {self.movie}"

class NowPlaying(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='now_playing_movies')

    def __str__(self):
        return f"Now Playing: {self.movie}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='bookings')
    num_tickets = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} booked {self.num_tickets} tickets for {self.movie}"

class Hall(models.Model):
    hall_id = models.IntegerField(primary_key=True)
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Hall {self.hall_id}"

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtime')
    show_date = models.DateField()
    show_time = models.TimeField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='showtimes')

    def __str__(self):
        return f"{self.movie} - {self.show_date} {self.show_time} - Hall {self.hall.hall_id}"
