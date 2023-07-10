from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse

# Create your views here.

def index(request):

#     if month in monthlyChallenges:
#         return JsonResponse({'challenge': monthlyChallenges[month]})
#         return HttpResponse(f'Your challenge for {month} is: {monthlyChallenges[month]}')
    return HttpResponse(f'<h1>welcome to the books app<h1>')

