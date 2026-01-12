from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from appointment.utils import get_reminders
from employee.models import Employee


class Command(BaseCommand):
    help = "Envoie un email si des reminders sont prévus pour aujourd'hui"

    def handle(self, *args, **options):
        reminders = get_reminders()
        today = timezone.now().date()
        reminders_today = [r for r in reminders if r['reminder_date'] == today]

        if not reminders_today:
            self.stdout.write(self.style.WARNING('Aucun reminder pour aujourd\'hui'))
            return

        # recipient_list = ["davide.calvaresi@hevs.ch", "renaud.richardet@hevs.ch"]
        recipient_list = [
            "aurelie.pham@students.hevs.ch",
            "grace.naing@students.hevs.ch",
            "karel-vilem.svoboda@students.hevs.ch",
        ]

        if not recipient_list:
            self.stdout.write(self.style.WARNING('Aucun employé avec email trouvé'))
            return

        subject = f"Reminders du {today.strftime('%d/%m/%Y')}"

        message = "Bonjour,\n\n"
        message += (
            f"Vous avez {len(reminders_today)} reminder(s) pour aujourd'hui :\n\n"
        )

        for reminder in reminders_today:
            item = reminder['item']
            animal = reminder['animal']
            appointment_date = reminder['original_date']
            message += f"- {item.name} pour {animal.name} (rendez-vous du {appointment_date.strftime('%d/%m/%Y')})\n"

        message += "\n\nCordialement,\nVet Software"

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Email envoyé avec succès à {len(recipient_list)} client(s)"
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Erreur lors de l'envoi du email: {str(e)}")
            )
