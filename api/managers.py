from django.contrib.auth.base_user import BaseUserManager




class MyUserManager(BaseUserManager):

    def create_user(self, email, password, is_teacher=False):

        if email is None:
            raise TypeError('ERROR: Users must have an email address.')
        if password is None:
            raise TypeError('ERROR: Users must have a password.')

        user = self.model(
            email=self.normalize_email(email),
            is_teacher=is_teacher
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email), 
            password=password
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save()

        return user