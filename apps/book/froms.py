from django import forms
from . import models


class AddBookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = "__all__"


class DateInput(forms.DateInput):
    input_type = "date"


class UpdateBookForm(AddBookForm):
    pass


class AddBookCopyForm(forms.ModelForm):
    class Meta:
        model = models.BookCopy
        fields = "__all__"
        exclude = ["book"]


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = "__all__"
        widgets = {"birth_date": DateInput(), "death_date": DateInput()}
