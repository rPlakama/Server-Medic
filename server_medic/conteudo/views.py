from django.http import HttpResponse


def conteudo_list(request):
    return HttpResponse("conteudo list")


def conteudo_create(request):
    return HttpResponse("conteudo create")


def conteudo_detail(request, pk):
    return HttpResponse(f"conteudo detail {pk}")