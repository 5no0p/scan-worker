from django.utils import timezone

from core.helper import datetime_defrences

def event_end_date():
    date_time = timezone.now()
    days = 2
    return datetime_defrences(date_time, days)

def event_category_end_date():
    date_time = timezone.now()
    minutes = 720
    return datetime_defrences(date_time, minutes=minutes)