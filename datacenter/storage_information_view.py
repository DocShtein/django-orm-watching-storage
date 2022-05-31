import datetime

from datacenter.models import Passcard
from datacenter.models import Visit, get_duration, format_duration, is_visit_long
from django.shortcuts import render



def storage_information_view(request):
    visits = Visit.objects.all()
    active_visits = visits.filter(leaved_at=None)
    print(is_visit_long(visits))

    for employee in active_visits:
        time_duration = get_duration(active_visits)
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
