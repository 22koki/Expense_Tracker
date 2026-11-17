from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.Model):
    KIND_CHOICES = [("income", "Income"), ("expense", "Expense")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=60)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default="expense")

    class Meta:
        ordering = ["kind", "name"]
        constraints = [models.UniqueConstraint(fields=["user", "name", "kind"], name="unique_user_category_kind")]

    def __str__(self):
        return f"{self.name} ({self.kind})"

class Transaction(models.Model):
    KIND_CHOICES = [("income", "Income"), ("expense", "Expense")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    date = models.DateField(default=timezone.localdate)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} — {self.amount}"
