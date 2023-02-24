from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField, ManyToManyField, TextChoices

from locations.models import Location


# ----------------------------------------------------------------
# User model
class User(AbstractUser):
    class Roles(TextChoices):
        ADMIN = 'admin', 'Администратор'
        MODERATOR = 'moderator', 'Модератор'
        MEMBER = 'member', 'Пользователь'

    password: CharField = CharField(max_length=200)
    role: CharField = CharField(max_length=15, choices=Roles.choices, default=Roles.MEMBER)
    age: IntegerField = IntegerField(default=0)
    locations: ManyToManyField = ManyToManyField(Location, default=[])

    class Meta:
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'

    def __str__(self):
        return self.username
