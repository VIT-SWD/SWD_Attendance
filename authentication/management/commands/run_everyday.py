from django.core.management.base import BaseCommand
from authentication.models import Volunteer

class Command(BaseCommand):
    help = "Reset marked_IN_attendance to False for all Volunteers daily"

    def handle(self, *args, **kwargs):
        Volunteer.objects.update(marked_IN_attendance=False)
        self.stdout.write("Attendance reset: marked_IN_attendance set to False for all volunteers.")
