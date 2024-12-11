from django import forms


class BucketUploadForm(forms.Form):
    image = forms.ImageField()


