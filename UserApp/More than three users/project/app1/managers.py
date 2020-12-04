from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_data):
        if not email:
            raise ValueError('email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_data)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_data):
        extra_data.setdefault('is_superuser', False)
        extra_data.setdefault('admin', False)
        extra_data.setdefault('staff', True)
        return self._create_user(email, password, **extra_data)

    def create_superuser(self, email, password, **extra_data):
        extra_data.setdefault('is_superuser', True)
        extra_data.setdefault('admin', True)
        extra_data.setdefault('staff', True)
        return self._create_user(email, password, **extra_data)
