from django.http import HttpResponse


def avaliacao_list(request):
    return HttpResponse("avaliacao list")


def avaliacao_detail(request, pk):
    return HttpResponse(f"avaliacao detail {pk}")