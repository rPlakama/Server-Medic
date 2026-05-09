from django.http import HttpResponse


def categoria_list(request):
    return HttpResponse("categoria list")


def categoria_detail(request, pk):
    return HttpResponse(f"categoria detail {pk}")