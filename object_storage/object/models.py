from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import re

class CustomUser(models.Model):
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': "نام کاربری انتخاب شده قبلا استفاده شده است.",
        },
    )

    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="ایمیل معتبر نیست.")],
        error_messages={
            'unique': "این ایمیل قبلا ثبت شده است.",
        },
    )

    password = models.CharField(
        max_length=128,
        validators=[],
    )

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        self.clean_username()
        self.clean_email()
        self.clean_password()

    def clean_username(self):
        if len(self.username) < 4:
            raise ValidationError('نام کاربری باید حداقل 4 کاراکتر باشد.')
        if not re.match("^[a-zA-Z]*$", self.username):
            raise ValidationError('نام کاربری باید فقط شامل حروف انگلیسی باشد.')
        if CustomUser.objects.exclude(pk=self.pk).filter(username=self.username.lower()).exists():
            raise ValidationError('نام کاربری انتخاب شده قبلا استفاده شده است.')

    def clean_email(self):
        if CustomUser.objects.exclude(pk=self.pk).filter(email=self.email.lower()).exists():
            raise ValidationError('این ایمیل قبلا ثبت شده است.')

    def clean_password(self):
        if len(self.password) < 6:
            raise ValidationError('رمز عبور باید حداقل 6 کاراکتر باشد.')
        if not re.search("[a-z]", self.password):
            raise ValidationError('رمز عبور باید شامل حداقل یک حرف کوچک باشد.')
        if not re.search("[A-Z]", self.password):
            raise ValidationError('رمز عبور باید شامل حداقل یک حرف بزرگ باشد.')
        if not re.search("[0-9]", self.password):
            raise ValidationError('رمز عبور باید شامل حداقل یک عدد باشد.')
        if not re.search("[@!#$%&]", self.password):
            raise ValidationError('رمز عبور باید شامل حداقل یک کاراکتر خاص مانند @!#$%& باشد.')

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.email.lower()
        self.first_name = self.first_name.lower()
        self.last_name = self.last_name.lower()
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'UserName: {self.username}, Email: {self.email}'
