from django.http import HttpResponse


def especialidade_list(request):
    return HttpResponse("especialidade list")


def especialidade_detail(request, pk):
    return HttpResponse(f"especialidade detail {pk}")