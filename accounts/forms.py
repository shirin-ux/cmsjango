from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

from accounts.models import Payments, Profile


class PaymentsForm(forms.ModelForm):
    class Meta:  # مدل فرم فرق ميكنه با فرم هاي ديگه كلاس متا متا ديتاهاي مربوط به مدل مي گيرد
        model = Payments
        fields = ['amount', 'transaction_code']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount % 1000 != 0:
            raise ValidationError('مقدار تراكنش بايد ضريبي از 1000 باشد')
        return amount

    def clean(self):
        super().clean()
        code = self.cleaned_data.get('transaction_code')
        amount = self.cleaned_data.get('amount')
        if amount is not None and code is not None:
            if int(code.split('-')[1]) != amount:
                raise ValidationError('مبلغ و رسيد تراكنش با هم همخواني ندارند')

    def clean_transaction_code(self):
        code = self.cleaned_data.get('transaction_code')
        try:
            assert code.startswith('bank-')
            assert code.endswith('#')
            parts = code.split('-')
            assert len(parts) == 3
            int(parts[1])
        except:
            raise ValidationError('قالب رسيد تراكنش معتبر نيست')
        return code


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile', 'gender', 'address', 'profile_image']


class MyUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name', 'email']

    password = None