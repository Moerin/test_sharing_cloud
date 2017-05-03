from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    """Form to create post """

    class Meta:
        model = Post
        fields = ('title', 'content',)  # visible field
        widgets = {
            'content': forms.Textarea(
                attrs={'id': 'post-content',
                       'required': True,
                       'placeholder': _('Say something...'),
                       'rows': '3',
                       'cols': '50',
                       'maxlength': '140',  # constraint for 140 character
                       'class': 'form-control'
                       }
            ),
            'title': forms.TextInput(
                attrs={'id': 'post-title',
                       'required': True,
                       'placeholder': _('Title of your message'),
                       'class': 'form-control'}
            ),
        }
