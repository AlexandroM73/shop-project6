# mailing/admin.py
from django.contrib import admin
from .models import Recipient, Message, Mailing, SendingAttempt


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment')
    search_fields = ('email', 'full_name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body_preview')
    search_fields = ('subject',)

    def body_preview(self, obj):
        # Чтобы в админке не тянулась вся длинная текстовая область
        return (obj.body[:50] + '…') if len(obj.body) > 50 else obj.body
    body_preview.short_description = 'Текст (превью)'


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'start_time', 'end_time', 'message_subject')
    list_filter = ('status',)
    search_fields = ('message__subject',)

    def message_subject(self, obj):
        return obj.message.subject
    message_subject.short_description = 'Тема письма'


@admin.register(SendingAttempt)
class SendingAttemptAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'recipient_email', 'status', 'attempt_time')
    list_filter = ('status',)
    date_hierarchy = 'attempt_time'

    def recipient_email(self, obj):
        return obj.recipient.email if obj.recipient else '—'
    recipient_email.short_description = 'Email получателя'
