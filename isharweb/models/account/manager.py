from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    """
    Account manager.
    """

    def create_user(self, email, account_name, password=None):
        """
        Creates and saves an Account with the given email address,
            account name, and password.
        """
        if not email:
            raise ValueError('E-mail address is required.')

        if not account_name:
            raise ValueError('Account name is required.')

        user = self.model(
            email=self.normalize_email(email),
            account_name=account_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, account_name, password=None):
        """
        Creates and saves an Account with the given email address,
            account name, and password.
        However, it will not be a "superuser", since no players.
        """
        user = self.create_user(
            email=email,
            account_name=account_name,
            password=password
        )
        user.save(using=self._db)
        return user
