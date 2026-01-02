from django.core.management.base import BaseCommand
from datetime import date, time
from employee.models import OpenHours


class Command(BaseCommand):
    help = 'Populate open hours for the veterinary clinic'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating open hours data...")

        # Define clinic open hours: Monday (0) to Friday (4)
        for day in range(5):
            # morning
            OpenHours.objects.create(
                start_date=date(2025, 1, 1),
                end_date=date(2025, 12, 31),
                day_of_week=day,
                start_time=time(8, 0),
                end_time=time(12, 0),
            )
            # afternoon
            OpenHours.objects.create(
                start_date=date(2025, 1, 1),
                end_date=date(2025, 12, 31),
                day_of_week=day,
                start_time=time(14, 0),
                end_time=time(18, 0),
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {OpenHours.objects.count()} open hour schedules"
            )
        )
