from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
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
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)  # افزودن فیلد last_login

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

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
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Id:{self.id} UserName: {self.username}, Email: {self.email}'

class TempUser(models.Model):
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
    password = models.CharField(max_length=128)
    raw_password = models.CharField(max_length=128, blank=True, null=True)  # فیلد جدید برای ذخیره پسورد خام
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.raw_password = raw_password  # ذخیره پسورد خام

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def get_raw_password(self):
        return self.password
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
        if len(self.raw_password) < 6:
            raise ValidationError('رمز عبور باید حداقل 6 کاراکتر باشد.')
        if not re.search("[a-z]", self.raw_password):
            raise ValidationError('رمز عبور باید شامل حداقل یک حرف کوچک باشد.')
        if not re.search("[A-Z]", self.raw_password):
            raise ValidationError('رمز عبور باید شامل حداقل یک حرف بزرگ باشد.')
        if not re.search("[0-9]", self.raw_password):
            raise ValidationError('رمز عبور باید شامل حداقل یک عدد باشد.')
        if not re.search("[@!#$%&]", self.raw_password):
            raise ValidationError('رمز عبور باید شامل حداقل یک کاراکتر خاص مانند @!#$%& باشد.')

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Id:{self.id} UserName: {self.username}, Email: {self.email}'