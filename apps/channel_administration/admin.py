from django.contrib import admin

from apps.channel_administration.models import ChannelAdmin


@admin.register(ChannelAdmin)
class ChannelAdminModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin', 'channel', 'percent')
    search_fields = ('id', 'channel__title', 'channel__id', 'admin__username')
    raw_id_fields = ('channel', 'admin',)
