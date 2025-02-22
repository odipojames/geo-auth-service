from django.contrib import admin
from .models import CustomUser as User
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class CustomAdminSite(admin.AdminSite):
    site_header = 'Geo Pay Admin'
    site_title = 'Admin Portal'
    index_title = 'Welcome to Geo Pay'


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "role", "is_active", "is_staff")

    def clean_password2(self):
        # Ensure that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on the user, but replaces the password field with admin's password hash display field."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "is_active", "is_staff")

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "first_name", "last_name", 'role')
    list_filter = ("first_name", "email")
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "role", "password")}),
        ("Contact info", {"fields": ("email",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "role", "is_active", "is_staff", "is_superuser", "password1", "password2"),
        }),
    )
    search_fields = ("email","first_name", "last_name", "role",)
    ordering = ("email",)
    filter_horizontal = ()


custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(User, UserAdmin)
#custom_admin_site.register(Group) 
