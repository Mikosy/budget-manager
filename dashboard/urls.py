from django.urls import path
from .views import *

app_name = "dashboard"

urlpatterns = [
    path('', index , name="home"),
    path('profile', user_profile , name="profile"),
    path('add_income/', add_income, name='add_income'),
    path('user_table/', user_table, name='user_table'),
    path('add_category/', add_category, name='add_category'),
    path('edit_category/<str:edit_cat>/', edit_category, name='edit_category'),
    path('edit_category/<str:budget_id>/', edit_budget, name='edit_budget'),
    path('delete_income/<str:income_id>/', delete_income, name='delete_income'),
]
