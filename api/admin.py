from django.contrib import admin
from .models import User, List, Task
# Register your models here.
admin.site.register(List)
admin.site.register(Task)