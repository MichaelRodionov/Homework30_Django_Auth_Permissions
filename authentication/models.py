from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField, ManyToManyField

from locations.models import Location


# ----------------------------------------------------------------
# User model
class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    MEMBER = 'member'
    ROLE = [(ADMIN, 'Администратор'), (MODERATOR, 'Модератор'), (MEMBER, 'Пользователь')]

    password: CharField = CharField(max_length=200)
    role: CharField = CharField(max_length=15, choices=ROLE, default=MEMBER)
    age: IntegerField = IntegerField(default=0)
    locations: ManyToManyField = ManyToManyField(Location, default=[])

    class Meta:
        verbose_name: str = 'Пользователь'
        verbose_name_plural: str = 'Пользователи'

    def __str__(self):
        return self.username
