from django.http import HttpResponse


def autor_list(request):
    return HttpResponse("autor list")


def autor_detail(request, pk):
    return HttpResponse(f"autor detail {pk}")