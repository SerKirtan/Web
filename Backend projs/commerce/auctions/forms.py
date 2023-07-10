from .models import  Auction_Listing, Bid, Comment
from django import forms

class ListingForm(forms.ModelForm):
    class Meta:
        model = Auction_Listing
        fields = [
            'item',
            'price',
            'image',
            'category',
            'duration',
        ]

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['comment']
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.visible_fields()[0].field.widget.attrs['class'] = 'form-control w-75 h-75'