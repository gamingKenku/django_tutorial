from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date
from hello.models import Book


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class BookStoreUserManager(BaseUserManager):
    def create_user(self, username, mail, first_name, password):
        if not username:
            raise ValueError("У пользователя должно быть имя.")

        user = self.model(username=username)
        user.set_password(password)
        user.first_name = first_name
        user.mail = self.normalize_email(mail)
        user.date_joined = date.today()
        user.save()
        return user

    def create_staff_user(self, username, mail, first_name, password):
        user = self.create_user(
            username, mail, first_name, password=password
        )
        user.is_staff = True
        user.save()

        return user

    def create_superuser(self, username, mail, first_name, password):
        user = self.create_user(
            username, mail, first_name, password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class BookStoreUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, default='Не указано')
    username = models.CharField(unique=True, max_length=50, default='Не указано')
    password = models.CharField(max_length=128)
    mail = models.CharField(unique=True, max_length=50)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(default=date.today)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'mail']

    objects = BookStoreUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'book_store_user'


class OrderHistory(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(BookStoreUser, on_delete=models.CASCADE, )
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    order_date = models.DateTimeField()

    class Meta:
        db_table = 'order_history'
