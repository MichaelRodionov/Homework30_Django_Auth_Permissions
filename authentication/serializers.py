from typing import Any

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from authentication.models import User, Location


# ----------------------------------------------------------------
# User serializers
class UserListDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for ListView and RetrieveView
    """
    locations: SerializerMethodField = SerializerMethodField()
    total_ads: serializers.IntegerField = serializers.IntegerField()

    class Meta:
        model: User = User
        fields: list[str] = ['id', 'first_name', 'last_name', 'username', 'email', 'age',
                             'total_ads', 'locations', 'date_joined', 'role']

    def get_locations(self, user) -> list:
        """
        Method to make list of locations
        :param user: object of user
        :return: list of locations
        """
        return [loc.name for loc in user.locations.all()]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for CreateView
    """
    id: serializers.IntegerField = serializers.IntegerField(required=False)
    locations: serializers.SlugRelatedField = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    def is_valid(self, raise_exception=False) -> bool:
        """
        Method to validate data
        :param raise_exception: False
        :return: bool
        """
        self._locations = self.initial_data.pop('locations', [])

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data) -> Any:
        """
        Method to create instance
        :param validated_data: validated data taken from request.body
        :return: user instance
        """

        user = super().create(validated_data)
        user.set_password(user.password)
        if self._locations:
            for location in self._locations:
                location_obj, _ = Location.objects.get_or_create(
                    name=location,
                    defaults={
                        'lat': 11.111111,
                        'lng': 11.111111
                    })
                user.locations.add(location_obj)
        user.save()
        return user

    class Meta:
        model: User = User
        fields = '__all__'


class UserChangeSerializer(serializers.ModelSerializer):
    """
    Serializer for UpdateView(update and partial update)
    """
    locations: serializers.SlugRelatedField = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    def is_valid(self, raise_exception=False) -> bool:
        """
        Method to validate data
        :param raise_exception: False
        :return: bool
        """
        if 'locations' in self.initial_data:
            self._locations = self.initial_data.pop('locations')

        return super().is_valid(raise_exception=raise_exception)

    def save(self) -> Any:
        """
        Method to save changes of user instance
        :return: user instance
        """
        user: Any = super().save()
        if 'locations' in self.initial_data:
            for location in self._locations:
                location_obj, _ = Location.objects.get_or_create(
                    name=location,
                    defaults={
                        'lat': 11.111111,
                        'lng': 11.111111
                    })
                user.locations.add(location_obj)
        user.save()

        return user

    class Meta:
        model: User = User
        exclude: list[str] = ['password']


class UserDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer for DeleteView
    """
    class Meta:
        model: User = User
        fields: list[str] = ['id']