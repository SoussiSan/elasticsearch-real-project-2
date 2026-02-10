from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name: str, last_name: str, email: str, username: str, password: str = None,
                    is_staff=False, is_superuser=False) -> 'User':
        if not email:
            raise ValueError('User must have an email')
        if not first_name:
            raise ValueError('User must have a first name')
        if not last_name:
            raise ValueError('User must have a last name')
        if not username:
            raise ValueError('User must have a username')
        if not password:
            raise ValueError('User must have a password')

        email = self.normalize_email(email)  # Normalise l'email (minuscules, etc.)
        user = self.model(username=username)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.set_password(password)  # Correction du typo : "set_passwod" → "set_password" (hachage sécurisé)
        user.is_active = True
        user.is_staff = is_staff  # Utilise le paramètre au lieu de le coder en dur
        user.is_superuser = is_superuser  # Utilise le paramètre au lieu de le coder en dur
        user.save(using=self._db)  # Ajout pour le support multi-base de données
        return user

    def create_superuser(self, first_name: str, last_name: str, email: str, username: str, password: str) -> 'User':
        # Crée un superutilisateur en forçant is_staff et is_superuser à True
        return self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
            is_staff=True,
            is_superuser=True
        )


class User(AbstractUser):
    # Suppression des redéfinitions des champs hérités (first_name, last_name, email, username, password)
    # Ils sont déjà dans AbstractUser ; les redéfinir peut causer des problèmes.
    country = models.CharField(verbose_name='Country', max_length=100,
                               blank=True)  # Ajout de max_length et rendu optionnel

    objects = UserManager()  # Assignation du manager personnalisé

    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'email']  # Correction : username est USERNAME_FIELD, password est séparé
    USERNAME_FIELD = 'username'
