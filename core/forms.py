from django import forms

from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):

    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:

        model = ContactMessage

        fields = (
            "name",
            "phone",
            "email",
            "subject",
            "message",
        )

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "placeholder": "نام شما",
                    "autocomplete": "name",
                    "maxlength": 100,
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "شماره تماس",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                    "maxlength": 20,
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "ایمیل شما",
                    "autocomplete": "email",
                    "maxlength": 254,
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "placeholder": "موضوع پیام",
                    "maxlength": 200,
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "placeholder": "پیام خود را بنویسید...",
                    "rows": 6,
                    "maxlength": 5000,
                }
            ),
        }

    def clean_name(self):

        name = self.cleaned_data["name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "نام باید حداقل ۲ کاراکتر باشد."
            )

        return name

    def clean_phone(self):

        phone = self.cleaned_data["phone"].strip()

        digits = "".join(
            character
            for character in phone
            if character.isdigit()
        )

        if len(digits) < 8 or len(digits) > 15:
            raise forms.ValidationError(
                "شماره تماس معتبر نیست."
            )

        return phone

    def clean_subject(self):

        subject = self.cleaned_data["subject"].strip()

        if len(subject) < 3:
            raise forms.ValidationError(
                "موضوع پیام باید حداقل ۳ کاراکتر باشد."
            )

        return subject

    def clean_message(self):

        message = self.cleaned_data["message"].strip()

        if len(message) < 10:
            raise forms.ValidationError(
                "متن پیام باید حداقل ۱۰ کاراکتر باشد."
            )

        return message

    def clean(self):

        cleaned_data = super().clean()

        website = cleaned_data.get("website")

        if website:
            raise forms.ValidationError(
                "ارسال فرم معتبر نیست."
            )

        return cleaned_data