from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from apps.account.models import User


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'full_name', 'username', 'phone', 'credit')
    search_fields = ('first_name', 'last_name', 'username', 'id', 'phone', 'email')
