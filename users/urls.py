from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('topMovies/' , views.ShowTopMovies , name = 'topMovies'),
    path('book_movie/', views.user_book_movie, name='book_movie'),
    path('book_movie/<int:movie_id>/', views.book_movie_detail, name='book_movie_detail1'),
    path('my_booked_movies/', views.user_booked_movies, name='my_booked_movies'),
    path('admin/custom-admin/', views.custom_admin_page, name='custom_admin_page'),
    path('admin/scrape-data/', views.scrape_data_view, name='scrape_data'),
    path('now_playing/', views.now_playing_movies, name='now_playing_movies'),
    path('admin/clear-lists/', views.clear_lists_view, name='clear_lists'),
    path('search/', views.showtime_search, name='showtime_search')
]
