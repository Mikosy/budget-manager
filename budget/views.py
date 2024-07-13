from django.shortcuts import render, redirect
from .models import *
from .forms import IncomeForm, ExpenseForm, BudgetForm
from decimal import Decimal
from django.contrib.auth.decorators import login_required


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    data = {
        'form': form
    }
    return render(request, 'budget/add_expenses.html', data)

def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()
    data = {
        'form': form
    }
    return render(request, 'budget/add_budget.html', data)


# def dashboard(request):
#     if request.user.is_authenticated:
#         incomes = Income.objects.filter(user=request.user)
#         expenses = Expenses.objects.filter(user=request.user)
#         budgets = Budget.objects.filter(user=request.user)
#         context = {
#             'incomes': incomes, 
#             'expenses': expenses, 
#             'budgets': budgets
#         }
#         return render(request, 'budget/dashboard.html', context)
#     return redirect('login')