from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Income)
admin.site.register(Expenses)
admin.site.register(Budget)