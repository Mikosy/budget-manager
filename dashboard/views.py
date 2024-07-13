from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from budget.models import *
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from budget.forms import *


@login_required
def index(request):
    budgets = Income.objects.filter(user=request.user).last()
    budget_split = Budget.objects.filter(user=request.user)
    categories = Category.objects.all()
    count_categories = categories.count()

    total_percentage = sum(cat.percentage for cat in categories)
    remaining_percentage = 100 - total_percentage

    args = {
        'budgets': budgets,
        'budget_split': budget_split,
        'categories': categories,
        'remaining_percentage': remaining_percentage,
        'count_categories': count_categories,
    }
    return render(request, 'dashboard/dashboard.html', args)


@login_required
def edit_budget(request, budget_id):
    budget = Budget.objects.get(id=budget_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        category.percentage += (amount / budget.amount) * 100
        category.save()
        budget.amount = amount
        budget.save()

        # Adjust other categories if necessary
        total_percentage = sum(cat.percentage for cat in categories)
        remaining_percentage = Decimal(100) - total_percentage

        if remaining_percentage > 0:
            for cat in categories:
                cat.percentage += (remaining_percentage / categories.count())
                cat.save()

        return redirect('dashboard:home')

    args = {
        'budget': budget,
        'categories': categories,
    }
    return render(request, 'dashboard/edit_budget.html', args)


@login_required
def add_income(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        source = request.POST['source']
        date = request.POST['date']
        user = request.user

        income = Income.objects.create(user=user, amount=amount, date=date, source=source)
        income.save()

        # Automatically split the income according to the predefined budget
        categories = Category.objects.all()
        for category in categories:
            split_amount = (category.percentage / Decimal(100)) * amount
            Budget.objects.create(user=user, amount=split_amount, period_start=date, period_end=date, category=category)

        return redirect('dashboard:add_income')

    return render(request, 'dashboard/add_income.html')


def user_profile(request):
    return render(request, 'dashboard/profile.html')


def user_table(request):
    budget_split = Budget.objects.filter(user=request.user)

    data = {
        'budget_split': budget_split,
    }

    return render(request, 'dashboard/tables.html', data)


def add_category(request):
    categories = Category.objects.all()

    total_percentage = sum(cat.percentage for cat in categories)
    remaining_percentage = 100 - total_percentage

    if request.method == 'POST':
        form = EditCategory(request.POST)
        if form.is_valid():
            form.save()
        messages.success(request, 'successfully added a category')
        return redirect('dashboard:add_category')

    args = {
        'categories': categories,
        'remaining_percentage': remaining_percentage
    }
    return render(request, 'dashboard/add_category.html', args)


def edit_category(request, edit_cat):
    category = get_object_or_404(Category, id=edit_cat)

    if request.method == 'POST':
        form = EditCategory(request.POST, instance=category)

        if form.is_valid():
            check_form = form.save(commit=False)
            check_form.save()
            messages.success(request, f'successfully changed {category}')
            return redirect('dashboard:home')

    return render(request, 'dashboard/edit-category.html')


@login_required
def delete_income(request, income_id):
    income = Income.objects.get(id=income_id, user=request.user)
    income.delete()
    return redirect('dashboard:home')
