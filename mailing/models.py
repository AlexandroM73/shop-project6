# mailing/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse

class Recipient(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    STATUS_CREATED = 'Создана'
    STATUS_RUNNING = 'Запущена'
    STATUS_COMPLETED = 'Завершена'

    STATUS_CHOICES = [
        (STATUS_CREATED, STATUS_CREATED),
        (STATUS_RUNNING, STATUS_RUNNING),
        (STATUS_COMPLETED, STATUS_COMPLETED),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
    )
    # Теперь Django точно видит класс Message, потому что он объявлен выше
    message = models.ForeignKey(Message, on_delete=models.PROTECT)
    recipients = models.ManyToManyField(Recipient, related_name='mailings')

    def update_status(self):
        now = timezone.now()
        old_status = self.status

        if now < self.start_time:
            new_status = self.STATUS_CREATED
        elif self.start_time <= now <= self.end_time:
            new_status = self.STATUS_RUNNING
        else:
            new_status = self.STATUS_COMPLETED

        if old_status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

    def __str__(self):
        return f"Рассылка #{self.id} ({self.status})"

    def get_absolute_url(self):
        return reverse('mailing_detail', kwargs={'pk': self.pk})


class SendingAttempt(models.Model):
    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Успешно', 'Успешно'),
            ('Не успешно', 'Не успешно'),
        ]
    )
    server_response = models.TextField(blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
    recipient = models.ForeignKey(
        Recipient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attempts'
    )

    def __str__(self):
        return f"{self.mailing} — {self.status}"
