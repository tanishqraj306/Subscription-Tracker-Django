from django.core.management.base import BaseCommand
from subscriptions.models import Subscription
from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Processes subscription bills, updates next billing dates, and sends alerts.'

    def handle(self, *args, **options):
        today = date.today()
        due_subscriptions = Subscription.objects.filter(next_billing_date__lte=today)

        if due_subscriptions:
            self.stdout.write(self.style.SUCCESS('Processing Due Subscriptions:'))
            for sub in due_subscriptions:
                # Send alert
                self.send_alert(sub)

                # Update next billing date
                self.update_next_billing_date(sub)

                self.stdout.write(self.style.SUCCESS(f'Processed {sub.name} for user {sub.user.username}'))
        else:
            self.stdout.write(self.style.SUCCESS('No due subscriptions to process.'))

    def send_alert(self, subscription):
        subject = f'Subscription Due: {subscription.name}'
        message = f'Your subscription for {subscription.name} is due today for ${subscription.price}.'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [subscription.user.email],
            fail_silently=False,
        )

    def update_next_billing_date(self, subscription):
        today = date.today()
        new_next_billing_date = subscription.next_billing_date

        while new_next_billing_date <= today:
            if subscription.billing_cycle == 'monthly':
                new_next_billing_date += relativedelta(months=1)
            elif subscription.billing_cycle == 'annually':
                new_next_billing_date += relativedelta(years=1)
            elif subscription.billing_cycle == 'weekly':
                new_next_billing_date += relativedelta(weeks=1)
            elif subscription.billing_cycle == 'daily':
                new_next_billing_date += relativedelta(days=1)
        
        subscription.next_billing_date = new_next_billing_date
        subscription.save()
