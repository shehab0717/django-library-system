from django import forms
from . import models


class AddBookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = "__all__"


class UpdateBookForm(AddBookForm):
    pass


class AddBookCopyForm(forms.ModelForm):
    class Meta:
        model = models.BookCopy
        fields = "__all__"
        exclude = ["book"]
