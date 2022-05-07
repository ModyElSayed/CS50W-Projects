from django import forms


class NewPage(forms.Form):
    title_name = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea())


class EditPage(forms.Form):
    title_name = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea())
