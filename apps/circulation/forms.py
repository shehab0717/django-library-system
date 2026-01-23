from django.forms import ModelForm, ChoiceField

from apps.circulation.models import CirculationRecord


class BorrowingCreateForm(ModelForm):
    period = ChoiceField(
        choices=[
            (3, "Three Days"),
            (5, "Five Days"),
            (7, "One Week"),
        ],
        initial=3,
        required=True,
        label="How long?",
    )

    class Meta:
        model = CirculationRecord
        fields = ["member"]

    @property
    def due_date(self):
        self.period
