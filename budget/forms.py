from django import forms
from .models import *

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'source']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['amount', 'date', 'category', 'description']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount', 'period_start', 'period_end', 'category']

class EditCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'percentage']