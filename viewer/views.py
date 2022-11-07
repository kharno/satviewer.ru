from django.http import JsonResponse
from django.shortcuts import render

from django.template.loader import render_to_string

from viewer.forms import *
from viewer.models import *
from .get_passes import *


def show_passes(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"html": render_to_string("viewer/passes.html", {'satpasses': get_passes(request.POST.dict())})})
    return render(request, 'viewer/index.html')
