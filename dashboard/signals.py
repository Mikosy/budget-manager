from django.db.models.signals import post_delete
from django.dispatch import receiver
from budget.models import Income, Expenses, Budget, Category


@receiver(post_delete, sender=Income)
def delete_related_records(sender, instance, **kwargs):
    user = instance.user
    expenses = Expenses.objects.filter(user=user)
    budgets = Budget.objects.filter(user=user)
    categories = Category.objects.all()

    expenses.delete()
    budgets.delete()
    categories.delete()
