from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    error_css_class = "login_form_error"
    username = forms.CharField(label="Username *", max_length=50, required=True, error_messages={'required':'Please enter your username.'})
    username.widget.attrs['class'] = "form-control"
    username.widget.attrs['id'] = "contact-form-username"

    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password *", error_messages={'required':'Please enter your password.'})
    password.widget.attrs['class'] = "form-control"
    password.widget.attrs['id'] = "contact-form-password"

class RegisterForm(UserCreationForm):
    error_messages = {
                        "password_mismatch": _("The two password fields didn’t match."),
                    }
    username = forms.CharField(label="Username *", max_length=50, required=True, error_messages={'required':'Please enter your desired username.'})
    username.widget.attrs['class'] = "form-control"
    username.widget.attrs['id'] = "contact-form-username"
    
    password1 = forms.CharField(
                    required=True,
                    label=_("Password"),
                    strip=False,
                    widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
                    help_text=password_validation.password_validators_help_text_html(),
                )
    password2 = forms.CharField(
                    required=True,
                    label=_("Password confirmation"),
                    widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
                    strip=False,
                    help_text=_("Enter the same password as before, for verification."),
                )

    #password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Password *", error_messages={'required':'Please enter your desired password.'})
    password1.widget.attrs['class'] = "form-control"
    password1.widget.attrs['id'] = "contact-form-password"

    #password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Re-enter Password *", error_messages={'required':'Please enter your desired password again.'})
    password2.widget.attrs['class'] = "form-control"
    password2.widget.attrs['id'] = "contact-form-password-two"

class QuoteForm(forms.Form):
    error_css_class = "quote_form_error" 

    name = forms.CharField(label="Name", label_suffix="", max_length=50, required=True, error_messages={'required':'Please enter your name.'})
    name.widget.attrs['class'] = "form-control"
    name.widget.attrs['id'] = "quote-form-name"
    name.widget.attrs['placeholder'] = "John Doe"

    email = forms.EmailField(label="Email", label_suffix="", max_length=50, required=True, error_messages={'required':'Please enter your email address.'})
    email.widget.attrs['class'] = "form-control"
    email.widget.attrs['id'] = "quote-form-email"
    email.widget.attrs['placeholder'] = "name@example.com"
    
    phone = forms.RegexField(label="Phone", label_suffix="", required=True, regex=r"1?\(?\d{3}\)?-? *\d{3}-? *-?\d{4}", error_messages={'required':'Please enter your phone number.', 'invalid':'Please enter a valid phone number.'})
    phone.widget.attrs['class'] = "form-control"
    phone.widget.attrs['id'] = "quote-form-phone"
    phone.widget.attrs['placeholder'] = "999-888-7777"

    vehicle = forms.CharField(label="Describe your vehicle", label_suffix="", widget=forms.Textarea, required=False)
    vehicle.widget.attrs['class'] = "form-control"
    vehicle.widget.attrs['id'] = ""
    vehicle.widget.attrs['placeholder'] = "Vehicle year, make and model"

    images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    images.widget.attrs['class'] = "form-control"
    images.widget.attrs['style'] = "display:none;"
    images.widget.attrs['id'] = "quote-form-images"
    images.widget.attrs['onchange'] = "imagesUploaded()"

    message = forms.CharField(label="Describe your project in detail", label_suffix="", widget=forms.Textarea, required=False)
    message.widget.attrs['class'] = "form-control"
    message.widget.attrs['id'] = "quote-form-message"
    message.widget.attrs['placeholder'] = "Message"

    def clean_phone(self):
        pass

class ContactForm(forms.Form):
    error_css_class = "quote_form_error" 
    
    name = forms.CharField(label="Name", label_suffix="", max_length=50, required=True, error_messages={'required':'Please enter your name.'})
    name.widget.attrs['class'] = "form-control"
    name.widget.attrs['id'] = "quote-form-name"
    name.widget.attrs['placeholder'] = "John Doe"

    email = forms.EmailField(label="Email", label_suffix="", max_length=50, required=True, error_messages={'required':'Please enter your email address.'})
    email.widget.attrs['class'] = "form-control"
    email.widget.attrs['id'] = "quote-form-email"
    email.widget.attrs['placeholder'] = "name@example.com"
    
    phone = forms.RegexField(label="Phone", label_suffix="", required=True, regex=r"\(?\d{3}\)?-? *\d{3}-? *-?\d{4}", error_messages={'required':'Please enter your phone number.', 'invalid':'Please enter a valid phone number.'})
    phone.widget.attrs['class'] = "form-control"
    phone.widget.attrs['id'] = "quote-form-phone"
    phone.widget.attrs['placeholder'] = "999-888-7777"

    message = forms.CharField(label="What would you like to talk about?", label_suffix="", widget=forms.Textarea, required=False)
    message.widget.attrs['class'] = "form-control"
    message.widget.attrs['id'] = "quote-form-message"
    message.widget.attrs['placeholder'] = "Message"

