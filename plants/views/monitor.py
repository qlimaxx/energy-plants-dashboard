from django.http import JsonResponse

from plants.tasks import save_data_from_monitor


def pull_data(request):
    save_data_from_monitor(**request.GET.dict())
    return JsonResponse({'success': True})
