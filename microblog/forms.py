from django import forms

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content',)
        widgets = {
            'content': forms.Textarea(
                attrs={'id': 'post-content',
                       'required': True,
                       'placeholder': 'Say something...',
                       'rows': '3',
                        'cols': '50',
                        'maxlength': '140',
                     }
            ),
            'title': forms.TextInput(
                attrs={'id': 'post-title', 'required': True, 'placeholder': 'Title of your message'}
            ),
        }
