from django.http import HttpResponse


def comentario_list(request):
    return HttpResponse("comentario list")


def comentario_detail(request, pk):
    return HttpResponse(f"comentario detail {pk}")