from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import strftime
from jdatetime import datetime as jd


class Profile(models.Model):
    class Meta:
        verbose_name = 'حساب كاربري',
        verbose_name_plural = 'حساب كاربري',

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='نمايه كاربري')
    mobile = models.CharField('تلفن همراه', max_length=11)
    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = ((MALE, 'مرد'), (FEMALE, 'زن'))
    gender = models.IntegerField('جنسيت', choices=GENDER_CHOICES, null=True, blank=True)
    brith_date = models.DateField('تاريخ تولد', null=True, blank=True)
    address = models.TextField('آدرس', null=True, blank=True)
    profile_image = models.ImageField('تصوير', upload_to='users/profile_images/', null=True, blank=True)
    balance = models.IntegerField('اعتبار', default=0)

    @property
    def jd_brith_date(self):
        return jd.fromgregorian(
            year=self.brith_date.year,
            month=self.brith_date.month,
            day=self.brith_date.day,
        )

    def __str__(self):
        return self.user.get_full_name()

    def get_balance_display(self):
        return ' {} تومان '.format(self.balance)

    def deposit(self, amount):
        self.balance += amount
        self.save()

    def spend(self, amount):
        if self.balance < amount:
            return False
        self.balance -= amount
        self.save()
        return True


class Payments(models.Model):
    class Meta:
        verbose_name = 'پرداخت',
        verbose_name_plural = 'پرداخت'

    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, verbose_name='كاربر')
    amount = models.PositiveIntegerField('مبلغ')
    transaction_time = models.DateTimeField('زمان تراكنش', auto_now_add=True)
    transaction_code = models.CharField('رسيد تراكنش', max_length=30)

    def __str__(self):
        return '{} تومان افزايش اعتيار براي {}'.format(self.amount, self.profile)

    @property
    def jd_transaction_time(self):
        return jd.fromgregorian(
            year=self.transaction_time.year,
            month=self.transaction_time.month,
            day=self.transaction_time.day,
            hour=self.transaction_time.hour,
            minute=self.transaction_time.minute,
            second=self.transaction_time.second,
        )