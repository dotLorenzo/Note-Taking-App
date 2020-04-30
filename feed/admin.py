from django.contrib import admin
from .models import Categories, Post

from autosave.mixins import AdminAutoSaveMixin

# @admin.register(Post)
class MyAdmin(AdminAutoSaveMixin, admin.ModelAdmin):
    # ...

    autosave_last_modified_field = 'date_posted'


admin.site.register(Categories)
admin.site.register(Post)