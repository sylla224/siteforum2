from django import forms
from django.core.exceptions import ValidationError

from forumapp.models import Forum, Category, MemberForum
from account.models import ForumUser


class ForumForm(forms.ModelForm):
    identifiant_category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Forum
        fields = ['nom', 'description', 'identifiant_category']
        exclude = ['slug']

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if len(nom) < 10:
            raise ValidationError('Le nom du forum doit avoir au minimun 10 caracteres')
        return nom


class LoginForm(forms.ModelForm):
    # username = forms.ModelChoiceField(queryset=ForumUser.objects.all())

    class Meta:
        model = MemberForum
        fields = ['forum', 'avatar']


class ConnexionForum(forms.ModelForm):
    class Meta:
        model = MemberForum
        fields = ['forum']
