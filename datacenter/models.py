from datetime import timedelta

from django.db import models
from django.utils.timezone import localtime
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit):
    local_entry_time = localtime(visit.entered_at)
    local_exit_time = localtime(visit.leaved_at)
    return (local_exit_time - local_entry_time).total_seconds()


def format_duration(duration):
    formatted_duration = str(timedelta(seconds=duration))
    hours, minutes, seconds = formatted_duration.split(':')
    return f'{hours} ч.{minutes} мин.'


def is_visit_long(visit, minutes=60):
    duration = get_duration(visit)
    duration_in_minutes = duration / 60

    if not visit.leaved_at:
        entry_time = localtime(visit.entered_at)
        now = localtime(timezone.now())
        time_delta_seconds = (now - entry_time).total_seconds()
        time_delta_minutes = time_delta_seconds / 60
        return time_delta_minutes > minutes
    else:
        return duration_in_minutes > minutes
