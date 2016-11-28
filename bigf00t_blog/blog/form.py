from django import forms

from .models import PostModel, ImageModle


class PostModelsForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = [
            'title',
            'content',
            'draft',
            'publishtime'
        ]


class ImageModelsForm(forms.ModelForm):
    class Meta:
        model = ImageModle
        fields = [
            'image',
        ]
