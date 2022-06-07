from datacenter.models import Passcard
from django.shortcuts import render
from django.utils import timezone
from datacenter.models import Visit, format_duration, is_visit_long
from django.utils.timezone import localtime


def storage_information_view(request):
    visits = Visit.objects.all()
    filtered_active_visits = visits.filter(leaved_at=None)
    serialized_visits = []

    for visit in filtered_active_visits:
        entry_time = localtime(visit.entered_at)
        now = localtime(timezone.now())
        time_delta = (now - entry_time).total_seconds()

        non_closed_visit = {
                'who_entered': visit.passcard.owner_name,
                'entered_at': localtime(visit.entered_at),
                'duration': format_duration(time_delta),
                'is_strange': is_visit_long(visit, minutes=60)
            }
        serialized_visits.append(non_closed_visit)

    context = {
        'non_closed_visits': serialized_visits,
    }

    return render(request, 'storage_information.html', context)

