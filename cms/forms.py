from django import forms


class CmspostSearchForm(forms.Form):
    name_post = forms.CharField(max_length=100, label='نام محصول', required=False)
    sale_is_open = forms.BooleanField(label='محصولات قابل فروش', required=False)

    PRICE_ANY = '0'
    PRICE_UNDER_10 = '1'
    PRICE_10_TO_15 = '2'
    PRICE_15_TO_20 = '3'
    PRICE_ABOVE_20 = '4'
    PRICE_LEVEL_CHOICES = (
        (PRICE_ANY, 'هر قيمتي'),
        (PRICE_UNDER_10, 'تا 10 هزار تومان'),
        (PRICE_10_TO_15, '10 تا 15 ميليون تومان'),
        (PRICE_15_TO_20, '15 تا 20 ميليون تومان'),
        (PRICE_ABOVE_20, 'بيش تر از 20 ميليون تومان'),
    )

    price_level = forms.ChoiceField(label='محدوده قيمت', choices=PRICE_LEVEL_CHOICES, required=False)

    # comment = forms.ModelChoiceField(label='نظرات', queryset=Cmscomment.objects.all(), required=False)  براي انواع محصولات يزاريم بعدا

    def get_price_boundries(self):
        price_level = self.cleaned_data['price_level']
        if price_level == CmspostSearchForm.PRICE_UNDER_10:
            return None, 10000
        elif price_level == CmspostSearchForm.PRICE_10_TO_15:
            return 1000000, 15000000
        elif price_level == CmspostSearchForm.PRICE_15_TO_20:
            return 15000000, 20000000
        elif price_level == CmspostSearchForm.PRICE_ABOVE_20:
            return 20000000, None
        else:
            return None, None
