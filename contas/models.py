from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import ResellerUserManager

class ResellerUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField('nome completo', max_length=150, blank=True)
    email = models.EmailField('e-mail', unique=True, null=True, blank=True)
    phone = models.CharField('telefone', max_length=20,
                             unique=True, null=True, blank=True)
    cupom_reseller = models.CharField('cupom revendedor', max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = ResellerUserManager()

    USERNAME_FIELD = 'email'                 # obrigatório mas não usado no login
    REQUIRED_FIELDS = []                     # usamos create_superuser(email,...)

    def __str__(self):
        return self.full_name or self.email or self.phone