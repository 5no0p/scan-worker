import datetime

def datetime_defrences(date_time, days=0, minutes=0, seconds=0, milliseconds=0):
    return date_time + datetime.timedelta(
        days=days,
        minutes=minutes,
        seconds=seconds,
        milliseconds=milliseconds
        )