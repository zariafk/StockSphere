from django import forms
from django.contrib.auth.models import User

# Form to create a new user
class CreateUserForm(forms.ModelForm):
    # Custom fields for user registration
    business_name = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    role = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True, label="Re-Enter Password")

    class Meta:
        model = User # Form will work with User model
        fields = ['business_name', 'username', 'email', 'role', 'password', 'password_confirm']

    # Custom validation for password confirmation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Check if passwords match
        if password and password_confirm and password != password_confirm:
            self.add_error("passowrd_confirm", "Passwords do not match.")
        return cleaned_data
    
    # Custom save method to create and save the User object
    def save(self, commit=True) -> User:
        # Create instance but do not save to database yet
        user = super().save(commit=False)
        # Populate fields
        user.business_name = self.cleaned_data["business_name"]
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        # Hash and set passowrd
        user.set_password(self.cleaned_data["password"])

        # Save user to database if commit = True
        if commit:
            user.save()
        return user
