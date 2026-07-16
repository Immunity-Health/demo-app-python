from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}))

    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email", "phone", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["phone"].initial = self.instance.phone
            self.fields["address"].initial = self.instance.address

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.phone = self.cleaned_data.get("phone", "")
        instance.address = self.cleaned_data.get("address", "")
        if commit:
            instance.save()
        return instance
