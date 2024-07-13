from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    source = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.source}: {self.amount}"


class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.category} - {self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period_start = models.DateField()
    period_end = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"

    def total_percentage(self):
        categories = Category.objects.all()
        total_percentage = sum(category.percentage for category in categories)
        return total_percentage
