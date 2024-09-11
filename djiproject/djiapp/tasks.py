from celery import shared_task
from .models import Flight_schedule, Subscription, Query
from django.utils import timezone

@shared_task
def update_status():
    current_time = timezone.now()
    entries = Flight_schedule.objects.filter(date__lt=current_time.date(), time__lt=current_time.time(), status=False)
    for entry in entries:
        entry.status = 1  # 或其他状态
        entry.save()