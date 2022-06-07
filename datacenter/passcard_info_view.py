from datacenter.models import Passcard, get_duration, format_duration, is_visit_long
from datacenter.models import Visit
from django.shortcuts import render


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    filtered_passcard_visits = Visit.objects.filter(passcard=passcard)
    serialized_passcard_visits = []

    for visit in filtered_passcard_visits:
        employee_visit = {
                'who_entered': visit.passcard.owner_name,
                'entered_at': visit.entered_at,
                'duration': format_duration(get_duration(visit)),
                'is_strange': is_visit_long(visit, minutes=60)
            }

        serialized_passcard_visits.append(employee_visit)

    context = {
        'passcard': passcard,
        'this_passcard_visits': serialized_passcard_visits

    }
    return render(request, 'passcard_info.html', context)
