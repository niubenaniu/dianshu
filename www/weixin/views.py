from django.shortcuts import render_to_response,render,RequestContext
from django.http import HttpResponse,Http404

# Create your views here.
def check_signature(request):
    
    return HttpResponse('ok')

