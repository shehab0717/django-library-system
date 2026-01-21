from django import forms
from . import models


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = "__all__"


class DateInput(forms.DateInput):
    input_type = "date"


class UpdateBookForm(BookCreateForm):
    pass


class BookCopyCreateForm(forms.ModelForm):
    class Meta:
        model = models.BookCopy
        fields = "__all__"
        exclude = ["book", "status"]


class AuthorCreateForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = "__all__"
        widgets = {"birth_date": DateInput(), "death_date": DateInput()}


class AuthorUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = "__all__"
        widgets = {"birth_date": DateInput(), "death_date": DateInput()}
