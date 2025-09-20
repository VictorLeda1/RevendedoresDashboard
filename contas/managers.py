from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

class ResellerUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, phone, password, **extra):
        if not email and not phone:
            raise ValueError('Informe email ou telefone.')
        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone=self._clean_phone(phone),
                          **extra)
        user.password = make_password(password)
        user.date_joined = timezone.now()
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone=None, password=None, **extra):
        extra.setdefault('is_staff', False)
        extra.setdefault('is_superuser', False)
        return self._create_user(email, phone, password, **extra)

    def create_superuser(self, email, password, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self._create_user(email, None, password, **extra)

    @staticmethod
    def _clean_phone(phone):
        if not phone:
            return None
        return ''.join(ch for ch in phone if ch.isdigit())