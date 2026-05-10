from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import Post

class PostForm(forms.ModelForm):
    imagen = CloudinaryFileField(
        options={
            'folder': "posts"
        },
        required=False
    )

    class Meta:
        model = Post
        fields = "__all__"
