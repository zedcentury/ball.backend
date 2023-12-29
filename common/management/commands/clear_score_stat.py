from django.core.management import BaseCommand

from score.models import ScoreStat


class Command(BaseCommand):
    def handle(self, *args, **options):
        ScoreStat.objects.all().delete()
