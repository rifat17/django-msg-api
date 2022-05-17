from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from rest_framework.authtoken.models import Token



class UsernameNotFoundError(Exception):
    def __init__(self, message='User should have a username'):
        self.message = message
        super().__init__(self.message)

class UserEmailNotFoundError(Exception):
    def __init__(self, message='User should have an email'):
        self.message = message
        super().__init__(self.message)

class PasswordNotFoundError(Exception):
    def __init__(self, message='User should have a password'):
        self.message = message
        super().__init__(self.message)

class UserCreationFailed(Exception):
    def __init__(self, message='User Creation Field'):
        self.message = message
        super().__init__(self.message)

                

class CustomUserManager(BaseUserManager):

    def create_user(self, username: str, email: str, password: str=None, **kwargs: dict):
        username = username.strip()
        email = email.strip()

        try:
            if username and email:
                user = self.model(
                    username=username,
                    email=self.normalize_email(email)
                )
                user.set_password(password)
                user.save()
                Token.objects.create(user=user)
                return user
            else:
                if not username:
                    raise UsernameNotFoundError()
                if not email:
                    raise UserEmailNotFoundError()
        except Exception as e:
            print(e)
            raise UserCreationFailed(str(e))


    def create_superuser(self, username, email, password=None):
        if password in None:
            raise PasswordNotFoundError()

        user = self.create_user(username=username,
                                email=self.normalize_email(email),
                                password=password)

        user.is_super = True
        user.is_staff = True
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username =  models.CharField(max_length=50, unique=True, db_index=True)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True) # by Default True
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return f'username: {self.username}, email: {self.email}'