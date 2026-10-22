# mailing/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Recipient, Message, Mailing, SendingAttempt
from .forms import MailingForm
from django.db.models import Count, Q
from django.core.cache import cache


DEFAULT_SENDER = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@shop-project.local')

# --- Recipient CRUD ---
class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'

class RecipientCreateView(CreateView):
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('recipient_list')

class RecipientUpdateView(UpdateView):
    model = Recipient
    fields = ['email', 'full_name', 'comment']
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('recipient_list')

class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient_list')


# --- Message CRUD ---
class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('message_list')

class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')


# --- Mailing CRUD + динамический статус ---
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'  # ← укажи свой шаблон
    context_object_name = 'mailing'               # ← в шаблоне будет переменная {{ mailing }}

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()  # вот тут вызывается твой метод из модели
        return obj


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing_list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')


# --- Отправка рассылки вручную (с batch-созданием попыток) ---
def start_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    now = timezone.now()

    # Проверка окна отправки
    if not (mailing.start_time <= now <= mailing.end_time):
        messages.error(request, "Отправка возможна только в интервале start_time–end_time.")
        return HttpResponseRedirect(mailing.get_absolute_url())

    mailing.update_status()

    attempts = []
    for recipient in mailing.recipients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=DEFAULT_SENDER,
                recipient_list=[recipient.email],
            )
            status = 'Успешно'
            response = 'OK'
        except Exception as e:
            status = 'Не успешно'
            response = str(e)

        # Добавляем в список, но НЕ пишем в БД сразу
        attempts.append(SendingAttempt(
            mailing=mailing,
            recipient=recipient,
            status=status,
            server_response=response,
        ))

    # Пакетная запись в БД — это и есть «batch» в Django
    SendingAttempt.objects.bulk_create(attempts)

    messages.success(request, f"Рассылка #{mailing.id} запущена. Созданы попытки отправки.")
    return HttpResponseRedirect(mailing.get_absolute_url())



# --- Дашборд (статистика) ---
class DashboardView(TemplateView):
    template_name = 'mailing/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = timezone.now()

        # Убрали кеш: считаем статистику каждый раз при заходе на страницу
        stats = SendingAttempt.objects.aggregate(
            total_attempts=Count('id'),
            success_attempts=Count('id', filter=Q(status='Успешно')),
            failed_attempts=Count('id', filter=Q(status='Не успешно')),
        )

        ctx.update(stats)

        ctx['total_mailings'] = Mailing.objects.count()
        ctx['active_mailings'] = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
        ).count()
        ctx['unique_recipients'] = Recipient.objects.count()

        return ctx


