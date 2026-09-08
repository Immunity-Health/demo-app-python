from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}))
    aadhar_number = forms.CharField(required=False)

    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email", "phone", "address", "aadhar_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["phone"].initial = self.instance.phone
            self.fields["address"].initial = self.instance.address
            self.fields["aadhar_number"].initial = self.instance.aadhar_number

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.phone = self.cleaned_data.get("phone", "")
        instance.address = self.cleaned_data.get("address", "")
        instance.aadhar_number = self.cleaned_data.get("aadhar_number", "")
        if commit:
            instance.save()
        return instance
