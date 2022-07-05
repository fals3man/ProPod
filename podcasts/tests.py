from django.test import TestCase
from django.utils import timezone
from .models import Episode
from django.urls.base import reverse
from datetime import datetime

class PodcastTests(TestCase):
	def setUp(self):
		self.Episode=Episode.objects.create(
			title="My First Podcast Episode",
			description="Checking",
			Publishing_Date=timezone.now(),
			link="https://myawesomeshow.com",
			image="https://image.myawesomeshow.com",
			Podcast_Name="My Podcast Project",
			guid="de194720-7b4c-49e2-a05f-432436d3fetr",
		)
	def test_episode_content(self):
		self.assertEqual(self.Episode.description, "Checking")
		self.assertEqual(self.Episode.link,"https://myawesomeshow.com")
		self.assertEqual(self.Episode.guid,"de194720-7b4c-49e2-a05f-432436d3fetr")
	
	def test_episode_representation(self):
		self.assertEqual(str(self.Episode),"My Podcast Project: My First Podcast Episode")
	
	def test_home_page_status_code(self):
		response=self.client.get("/")
		self.assertEqual(response.status_code,200)

	def test_home_page_uses_correct_template(self):
		response=self.client.get(reverse("homepage"))
		self.assertTemplateUsed(response,"homepage.html")

	def test_homepage_list_contents(self):
		response=self.client.get(reverse("homepage"))
		self.assertContains(response, "My First Podcast Episode")

