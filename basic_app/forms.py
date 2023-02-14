from django import forms
from basic_app.models import Post, Comment


class PostForm(forms.ModelForm):
    # What can be edited
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')

        # Add Widgets -> style for me to change the basic shape of django
        # textinputclass & postcontent both are my CSS classs
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):
    # What can be edited
    class Meta:
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
