from django.http import HttpResponse


def usuario_list(request):
    return HttpResponse("usuario list")


def usuario_create(request):
    return HttpResponse("usuario create")


def usuario_detail(request, pk):
    return HttpResponse(f"usuario detail {pk}")