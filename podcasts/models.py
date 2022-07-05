from django.db import models
class Episode(models.Model):
	title=models.CharField(max_length=600)
	description=models.TextField()
	Publishing_Date=models.DateTimeField()
	link=models.URLField()
	image=models.URLField()
	Podcast_Name=models.CharField(max_length=500)
	guid=models.CharField(max_length=50)

	def __str__(self) -> str:
		return f"{self.Podcast_Name}: {self.title}"
