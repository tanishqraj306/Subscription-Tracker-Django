import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from subscriptions.models import Subscription
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds the database with random data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding database...'))

        # Create users
        for i in range(3):
            username = f'user{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=f'user{i+1}@example.com', password='password')
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))

                # Create subscriptions for each user
                for j in range(5):
                    subscription_name = f'Subscription {j+1} for {username}'
                    price = round(random.uniform(5.0, 50.0), 2)
                    billing_cycle = random.choice(['daily', 'weekly', 'monthly', 'annually'])
                    next_billing_date = date.today() + timedelta(days=random.randint(-30, 30))

                    Subscription.objects.create(
                        user=user,
                        name=subscription_name,
                        price=price,
                        billing_cycle=billing_cycle,
                        next_billing_date=next_billing_date
                    )
                    self.stdout.write(self.style.SUCCESS(f'  - Created subscription: {subscription_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'User {username} already exists. Skipping.'))

        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))
