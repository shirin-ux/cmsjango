from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Cmspost(models.Model):
    """
    Represnt a post

    """

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست'

    name_post = models.CharField('عنوان', max_length=50)
    matn_post = models.TextField('متن')
    date_post = models.DateTimeField('زمان و تاريخ')
    image = models.ImageField('عكس', upload_to='post_images/')
    price_post = models.IntegerField('قيمت')
    shortage_post = models.IntegerField('كمبود محصول')
    sales_post = models.IntegerField('فروش محصول')
    SALE_NOT_STARTED = 1
    SALE_OPEN = 2
    SALE_CLOSED = 3
    POST_SOLD = 4
    status_choices = (
        (SALE_NOT_STARTED, 'به فروش نرسيده'),
        (SALE_OPEN, 'روانه بازار شده '),
        (SALE_CLOSED, 'اتمام موجودي'),
        (POST_SOLD, 'فروش محصول')
    )
    status = models.IntegerField('وضعيت', choices=status_choices, default=SALE_OPEN)

    def get_price_post_display(self):
        return ' {} تومان'.format(self.price_post)

    def reserve_shop(self, shop_count):
        assert isinstance(shop_count, int) and shop_count > 0, 'Numer NOT post cmspost'
        assert self.status == Cmspost.SALE_OPEN, 'SALE IS NOT OPEN'
        assert self.sales_post >= shop_count
        self.sales_post -= shop_count
        if self.shortage_post == 0:
            self.status = Cmspost.SALE_CLOSED
        self.save()

    def __str__(self):
        return self.name_post

    def total_price(self, amount):
        self.total_price(amount)
        self.save()


@login_required
class Cmscomment(models.Model):
    """
    Repersent a comment
    """

    class Meta:
        verbose_name = 'نظرات'
        verbose_name_plural = 'نظرات'

    matn_comment = models.TextField('متن نظرات')
    cmspost = models.ForeignKey('Cmspost', on_delete=models.PROTECT, verbose_name='عنوان')
    profile = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE, verbose_name='كاربر')

    def __str__(self):
        return self.matn_comment.title


class Shopping(models.Model):
    class Meta:
        verbose_name = 'خريد',
        verbose_name_plural = 'خريد',

    product = models.ForeignKey('Cmspost', on_delete=models.PROTECT, verbose_name='محصول')
    customer = models.ForeignKey('accounts.Profile', on_delete=models.PROTECT, verbose_name='خريدار')
    shop_count = models.IntegerField('تعداد خريد')  # تعدادخريد هر محصول
    order_time = models.DateTimeField('زمان خريد', auto_now_add=True)

    def __str__(self):
        return "{} خريد به نام {} براي محصول {}".format(self.shop_count, self.customer, self.product.name_post)
