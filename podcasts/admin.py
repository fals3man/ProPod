from django.contrib import admin

from .models import Episode
@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
	list_display=("Podcast_Name","title","Publishing_Date")
