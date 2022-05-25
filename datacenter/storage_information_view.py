import datetime

from datacenter.models import Passcard
from datacenter.models import Visit
from django.utils.timezone import localtime
from django.shortcuts import render


def get_duration(visit):
    all_employee_time_list = []
    for local_time in visit:
        local_entry_time = localtime(local_time.entered_at)
        local_exit_time = localtime(local_time.leaved_at)
        duration = local_exit_time - local_entry_time
        all_employee_time_list.append(duration)
    return all_employee_time_list


def format_duration(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds


def storage_information_view(request):
    employee_visits = Visit.objects.all()

    for employee in employee_visits:
        time_duration = get_duration(employee_visits)
        for employee_time in time_duration:
            hours, minutes, seconds = format_duration(employee_time)
            duration = f'{hours} ч. {minutes} мин.'
        non_closed_visits = [
            {
                'who_entered': employee.passcard.owner_name,
                'entered_at': employee.entered_at,
                'duration': duration,
            }
        ]

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
