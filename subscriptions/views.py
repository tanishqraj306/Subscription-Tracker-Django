from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Subscription
from .forms import SubscriptionForm, UserRegistrationForm
from datetime import date
from dateutil.relativedelta import relativedelta

@login_required(login_url='/subscriptions/login/')
def subscription_list(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions/subscription_list.html', {'subscriptions': subscriptions})

@login_required(login_url='/subscriptions/login/')
def monthly_subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user, billing_cycle='monthly')
    return render(request, 'subscriptions/monthly_subscriptions.html', {'subscriptions': subscriptions})

@login_required(login_url='/subscriptions/login/')
def yearly_subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user, billing_cycle='annually')
    return render(request, 'subscriptions/yearly_subscriptions.html', {'subscriptions': subscriptions})

@login_required(login_url='/subscriptions/login/')
def dashboard(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    total_subscriptions = subscriptions.count()
    upcoming_bills = subscriptions.filter(next_billing_date__gte=date.today()).order_by('next_billing_date')
    overdue_bills = subscriptions.filter(next_billing_date__lt=date.today()).order_by('next_billing_date')

    monthly_spending_only = sum(sub.price for sub in subscriptions if sub.billing_cycle == 'monthly')
    yearly_spending_only = sum(sub.price for sub in subscriptions if sub.billing_cycle == 'annually')
    weekly_spending_only = sum(sub.price for sub in subscriptions if sub.billing_cycle == 'weekly')
    daily_spending_only = sum(sub.price for sub in subscriptions if sub.billing_cycle == 'daily')

    # Calculate total monthly spending including prorated yearly, weekly, and daily
    monthly_spending = monthly_spending_only + (yearly_spending_only / 12) + (weekly_spending_only * 4) + (daily_spending_only * 30)

    # Calculate total yearly spending including prorated monthly, weekly, and daily
    yearly_spending = yearly_spending_only + (monthly_spending_only * 12) + (weekly_spending_only * 52) + (daily_spending_only * 365)

    context = {
        'total_subscriptions': total_subscriptions,
        'upcoming_bills': upcoming_bills,
        'overdue_bills': overdue_bills,
        'monthly_spending': round(monthly_spending, 2),
        'yearly_spending': round(yearly_spending, 2),
    }
    return render(request, 'subscriptions/dashboard.html', context)

@login_required(login_url='/subscriptions/login/')
def add_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('subscriptions:subscription_list')
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/add_subscription.html', {'form': form})

@login_required(login_url='/subscriptions/login/')
def mark_as_paid(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
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
    return redirect('subscriptions:dashboard')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('subscriptions:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'subscriptions/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('subscriptions:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'subscriptions/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('subscriptions:login')
