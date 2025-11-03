from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    BILLING_CYCLE_CHOICES = [
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
        ('weekly', 'Weekly'),
        ('daily', 'Daily'),
    ]
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CYCLE_CHOICES)
    next_billing_date = models.DateField()

    def __str__(self):
        return self.name