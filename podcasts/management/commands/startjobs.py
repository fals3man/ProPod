# Standard Library
import logging

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# Third Party
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from podcasts.models import Episode

logger = logging.getLogger(__name__)

def save_new_episodes(feed):
	# To save new episodes in db, check against the GUID currently stored,
	# If not found, add a new episode
	podcast_title=feed.channel.title
	podcast_image=feed.channel.image["href"]

	for item in feed.entries:
		if not Episode.objects.filter(guid=item.guid).exists():
			ep=Episode(
				title=item.title,
				description=(item.description),
				Publishing_Date=parser.parse(item.published),
				link=item.link,
				image=podcast_image,
				Podcast_Name=podcast_title,
				guid=item.guid,
			)
			ep.save()

def fetch_LexFridman_episodes():
	feed1=feedparser.parse("https://lexfridman.com/feed/podcast/")
	save_new_episodes(feed1)

def fetch_TheKnowledgeProject_episodes():
	feed2=feedparser.parse("https://theknowledgeproject.libsyn.com/rss")
	save_new_episodes(feed2)

def delete_old_job_executions(max_age=604_800):
	DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
	help="Runs apscheduler."

	def handle(self,*args,**options):
		scheduler= BlockingScheduler(timezone=settings.TIME_ZONE)
		scheduler.add_jobstore(DjangoJobStore(),"default")
		scheduler.add_job(
			fetch_TheKnowledgeProject_episodes,
			trigger="interval",
			minutes=2,
			id="The Knowledge Project Podcast",
			max_instances=1,
			replace_existing=True,
		)
		logger.info("Added job: The Knowledge Project Podcast.")

		scheduler.add_job(
			fetch_LexFridman_episodes,
			trigger="interval",
			minutes=2,
			id="Lex Fridman Podcast",
			max_instances=1,
			replace_existing=True,
		)
		logger.info("Added job: Lex Fridman Podcast.")

		scheduler.add_job(
			delete_old_job_executions,
			trigger=CronTrigger(
				day_of_week="mon",hour="00",minute="00" 
			),
			id="Delete Old Job Executions",
			max_instances=1,
			replace_existing=True,
		)
		logger.info("Added weekly job: Delete Old Job Executions.")
		try:
			logger.info("Strarting Scheduler...")
			scheduler.start()
		except KeyboardInterrupt:
			logger.info("Stopping Scheduler...")
			scheduler.shutdown()
			logger.info("Schedule shutdown successfully!")

		