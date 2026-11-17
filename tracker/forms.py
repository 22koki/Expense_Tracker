from django import forms
from .models import Category, Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["title", "amount", "kind", "category", "date", "note"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Monthly salary"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "min": "0.01", "step": "0.01", "placeholder": "0.00"}),
            "kind": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional details"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["category"].queryset = Category.objects.filter(user=user) if user else Category.objects.none()
        self.fields["category"].required = False

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    def clean(self):
        cleaned = super().clean()
        category = cleaned.get("category")
        kind = cleaned.get("kind")
        if category and self.user and (category.user_id != self.user.id or category.kind != kind):
            self.add_error("category", "Choose a category that belongs to you and matches the transaction type.")
        return cleaned

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "kind"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category name"}), "kind": forms.Select(attrs={"class": "form-select"})}
