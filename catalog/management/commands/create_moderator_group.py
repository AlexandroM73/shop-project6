# catalog/management/commands/create_moderator_group.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" и назначает ей права'

    def handle(self, *args, **options):
        group_name = 'Модератор продуктов'
        group, created = Group.objects.get_or_create(name=group_name)

        content_type = ContentType.objects.get_for_model(Product)

        # Получаем кастомное право
        unpublish_perm = Permission.objects.filter(
            codename='can_unpublish_product',
            content_type=content_type
        ).first()

        # Получаем стандартное право на удаление
        delete_perm = Permission.objects.filter(
            codename='delete_product',
            content_type=content_type
        ).first()

        if unpublish_perm and delete_perm:
            group.permissions.add(unpublish_perm, delete_perm)
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" успешно создана!'))
        else:
            self.stdout.write(self.style.ERROR('Ошибка: не найдены необходимые права. Проверьте миграции.'))
