import random
import functools

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def __create_user(
            self,
            mobile_phone,
            password=None,
            is_staff=False,
            is_active=False,
            is_superuser=False,
    ):
        user = self.model(
            mobile_phone=mobile_phone,
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_user(self, mobile_phone, password, **kwargs):
        return self.__create_user(
            mobile_phone,
            password,
            is_staff=kwargs.get("is_staff", False),
            is_active=kwargs.get("is_active", False),
            is_superuser=kwargs.get("is_superuser", False),
        )

    def create_superuser(self, mobile_phone, password):
        return self.__create_user(
            mobile_phone, password, is_staff=True, is_active=True, is_superuser=True
        )

    def create(self, **kwargs):
        """
        Important to have this to get factories working by default
        """
        mobile_phone = kwargs.get("mobile_phone")
        if not mobile_phone:
            raise ValueError("Users must have an mobile phone")
        return self.create_user(**kwargs)

    def create_for_person(self, person, password=None, is_active=False, **kwargs):
        if not password:
            password = self.make_random_password(length=6)

        user = self.create_user(
            mobile_phone=None, password=password, person=person, is_active=is_active, **kwargs
        )

        return user, password
