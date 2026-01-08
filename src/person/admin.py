from django.contrib import admin
from django import forms
from .models import Person


class PersonAdminForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True,
        help_text="Laissez vide pour conserver le mot de passe actuel",
    )

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'phone', 'email', 'birthday']

    def save(self, commit=True):
        person = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            person.set_password(password)

        if commit:
            person.save()
        return person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    form = PersonAdminForm
    list_display = ['first_name', 'last_name', 'phone', 'email', 'birthday']
    exclude = ['password_hash']
