from datacenter.models import Passcard, get_duration, format_duration, is_visit_long
from datacenter.models import Visit
from django.shortcuts import render


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.all()
    employee_passcard = passcard.get(passcode=passcode)
    visits = Visit.objects.filter(passcard=employee_passcard)
    for visit in visits:
        time_duration = get_duration(visit)
        hours, minutes, seconds = format_duration(time_duration)
        duration = f'{hours} ч. {minutes} мин.'
        flag = is_visit_long(visit, minutes=60)
        this_passcard_visits = [
            {
                'who_entered': visit.passcard.owner_name,
                'entered_at': visit.entered_at,
                'duration': duration,
                'is_strange': flag
            },
        ]
        context = {
            'passcard': visit,
            'this_passcard_visits': this_passcard_visits

        }
    return render(request, 'passcard_info.html', context)
