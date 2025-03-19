from django import forms
from django.contrib.auth.models import User

#User = get_user_model()

class CreateUserForm(forms.ModelForm):
    business_name = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    role = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True, label="Re-Enter Password")

    class Meta:
        model = User
        fields = ['business_name', 'username', 'email', 'role', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("passowrd_confirm", "Passwords do not match.")
        return cleaned_data
    
    def save(self, commit=True) -> User:
        user = super().save(commit=False)
        user.business_name = self.cleaned_data["business_name"]
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
