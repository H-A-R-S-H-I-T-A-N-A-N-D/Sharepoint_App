from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldnames in ['username', 'first_name', 'last_name', 'email', 'password2']:
            self.fields[fieldnames].help_text = None
        self.fields['password1'].help_text = "Password should be 15 chars length, should contain at least 1 - number, " \
                                             "upper case character,lower case character and special character. "

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
        # help_texts = {
        #     'username': None,
        #     'first_name': None,
        #     'last_name': None,
        #     'email': None,
        #     'password1': None,
        #     'password2': None,
        # }


# Profile Form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
