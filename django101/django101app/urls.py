from django.urls import path
from . import views # . means same directory

urlpatterns = [
    path('<int:month>', views.monthlyChallengeByDigit), # dynamic segments
    path('<str:month>', views.monthlyChallenge, name='monthlyChallenge'), # pathconverters: value type of the dynamic segments
]