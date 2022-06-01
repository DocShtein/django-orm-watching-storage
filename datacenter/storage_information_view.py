import datetime

from datacenter.models import Passcard
from datacenter.models import Visit, get_duration, format_duration, is_visit_long
from django.shortcuts import render



def storage_information_view(request):
    visits = Visit.objects.all()
    active_visits = visits.filter(leaved_at=None)

    for visit in active_visits:
        time_duration = get_duration(visit)
        hours, minutes, seconds = format_duration(time_duration)
        duration = f'{hours} ч. {minutes} мин.'
        flag = is_visit_long(visit, minutes=60)
        non_closed_visits = [
            {
                'who_entered': visit.passcard.owner_name,
                'entered_at': visit.entered_at,
                'duration': duration,
                'is_strange': flag
            }
        ]

    context = {
        'non_closed_visits': non_closed_visits,
    }

    return render(request, 'storage_information.html', context)

