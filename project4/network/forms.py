from django import forms


class NewPost(forms.Form):
    post_content = forms.CharField(label='', max_length=255, widget=forms.Textarea(attrs={'id': 'new-post-content',
                                                                                      'class': 'form-control',
                                                                                      'placeholder': 'Say it loud'}))
