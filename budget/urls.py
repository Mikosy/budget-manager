from django.urls import path
from budget.views import *

app_name = 'budget'

urlpatterns = [
    # path('', dashboard, name='dashboard'),
    path('add_expense/', add_expense, name='add_expense'),
    path('add_budget/', add_budget, name='add_budget'),
]