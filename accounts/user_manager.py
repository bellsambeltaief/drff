from django.contrib.auth.models import  BaseUserManager

class UserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for authorization
    instead of usernames. The default that's used is "UserManager"
    """

    def _create_user(self, email, password, staff=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        if staff:
            user = self.model(email=email, is_staff=True, is_superuser=True, **extra_fields)
        else:
            user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password,
                                 **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        staff = True
        return self._create_user(email, password, staff, **extra_fields)
