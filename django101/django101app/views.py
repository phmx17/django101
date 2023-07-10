from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse

monthlyChallenges = {
    'jan': 'eat more meat',
    'feb': 'study more comp sci',
    'mar': 'drink less booze'
}
# Create your views here.

def monthlyChallenge(request, month):
    if month in monthlyChallenges:
        return JsonResponse({'challenge': monthlyChallenges[month]})
#         return HttpResponse(f'Your challenge for {month} is: {monthlyChallenges[month]}')
    return HttpResponseNotFound(f'<h1>month {month} does not exist<h1>')

def monthlyChallengeByDigit(request, month):
    # create a redirect; response code = 302
    months = list(monthlyChallenges.keys())
    if month > len(months) or month <= 0:
        return HttpResponseNotFound(f'<h1>month {month} does not exist<h1>')

    redirectMonth = months[month-1]
    redirectPath = reverse('monthlyChallenge', args=[redirectMonth]) # pass name of path and the dyn segment
    return HttpResponseRedirect(redirectPath) # full path!
