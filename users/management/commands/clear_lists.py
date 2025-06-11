from typing import Any
from django.core.management.base import BaseCommand, CommandError
from users.models import *
import shutil
from django.conf import settings
import os
def delete_directory(directory_path):
    try:
        shutil.rmtree(directory_path)
    except OSError as e:
        raise CommandError(f"Error occurred while deleting directory '{directory_path}': {e}")

class Command(BaseCommand):
    help = 'clear movies tables'
    def handle(self, *args: Any, **options: Any):
        Movie.objects.all().delete() 
        TopMovie.objects.all().delete()
        NowPlaying.objects.all().delete()
        # delete_directory(os.path.join(settings.MEDIA_ROOT, "images"))

