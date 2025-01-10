from django import forms

from AuthApp.models import CustomUser


class CustomUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password"
    )

    password_confirmed = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password"
    )

    role = forms.ChoiceField(
        widget=forms.Select(),
        initial=CustomUser.Role.USER,
        choices=CustomUser.Role.choices,
        label="Role"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmed = cleaned_data.get('password_confirmed')
        if password != password_confirmed:
            self.add_error('password_confirmed', 'Passwords do not match')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            self.add_error("username", f"User with {username} exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            self.add_error("email", f"User with {email} exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=128, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not CustomUser.objects.filter(username=username).exists():
            self.add_error('username', f'User with {username} does not exist')
        return username

class CustomUpdateForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'id_old_password',}),
        label = "Old Password",
        required=True
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'id_new_password',}),
        label="New Password",
        required=True
    )

    new_password_confirmed = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'id_new_password_confirmed',}),
        label="Confirm New Password",
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password', 'new_password_confirmed']

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        new_password_confirmed = cleaned_data.get('new_password_confirmed')

        if not self.instance.check_password(old_password):
            self.add_error('old_password', 'Old Password is not correct')

        if new_password != new_password_confirmed:
            self.add_error('new_password_confirmed', 'New password do not match')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('new_password'):
            user.set_password(self.cleaned_data['new_password'])

        if commit:
            user.save()
        return user
