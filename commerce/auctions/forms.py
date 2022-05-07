from django import forms
from .models import *


class ListingsForm(forms.Form):
    title = forms.CharField(label='Title', max_length=32, widget=forms.TextInput(attrs={
        'class': "form-control", 'id': "floatingTitle", 'placeholder': "title",
    }))
    description = forms.CharField(label='Description', max_length=256, widget=forms.Textarea(attrs={
        'class': "form-control", 'id': "floatingDescription", 'placeholder': "description",
    }))
    starting_bid = forms.FloatField(label="Starting Bid", widget=forms.TextInput(attrs={
        'type': 'number', 'class': 'form-control', 'min': '0', 'step': '0.01',
        'id': "floatingBid", 'placeholder': "bid",
    }))

    category = forms.CharField(widget=forms.Select(choices=AuctionListings.Category.choices, attrs={
        'class': "form-control", 'id': "floatingInput", 'placeholder': "category",
    }))
    image_url = forms.URLField(label='Image URL', max_length=256, required=False, widget=forms.TextInput(attrs={
        'type': 'url', 'class': "form-control", 'id': "floatingURL", 'placeholder': "url",
    }))


class CommentForm(forms.Form):
    comment_area = forms.CharField(label='', max_length=256, widget=forms.Textarea(attrs={
        'class': "form-control", 'placeholder': "Leave a comment here", 'style': "height: 100px",
        'id': "floatingTextarea2",
    }))


class BidForm(forms.Form):
    bid = forms.FloatField(label="", widget=forms.TextInput(
        attrs={'type': 'number', 'class': 'form-control', 'min': '0',
               'step': '0.01', 'name': "bid", 'placeholder': "Bid"}))


class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['watchlist', 'user']
        exclude = ['date_added']
