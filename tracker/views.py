import csv
from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import CategoryForm, TransactionForm
from .models import Category, Transaction

def home(request):
    return redirect("dashboard") if request.user.is_authenticated else redirect("login")

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account is ready. Welcome to PennyWise!")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})

@login_required
def dashboard(request):
    today = timezone.localdate()
    month_transactions = Transaction.objects.filter(user=request.user, date__year=today.year, date__month=today.month)
    all_transactions = Transaction.objects.filter(user=request.user)
    income = month_transactions.filter(kind="income").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    expenses = month_transactions.filter(kind="expense").aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    category_totals = list(month_transactions.filter(kind="expense", category__isnull=False).values("category__name").annotate(total=Sum("amount")).order_by("-total")[:6])
    monthly = []
    for month in range(1, 13):
        rows = all_transactions.filter(date__year=today.year, date__month=month)
        monthly.append({
            "label": date(today.year, month, 1).strftime("%b"),
            "income": float(rows.filter(kind="income").aggregate(v=Sum("amount"))["v"] or 0),
            "expense": float(rows.filter(kind="expense").aggregate(v=Sum("amount"))["v"] or 0),
        })
    context = {
        "income": income, "expenses": expenses, "balance": income - expenses,
        "recent": all_transactions[:6], "monthly_json": monthly,
        "category_json": [{"name": x["category__name"], "total": float(x["total"])} for x in category_totals],
        "month_name": today.strftime("%B %Y"),
    }
    return render(request, "tracker/dashboard.html", context)

@login_required
def transaction_list(request):
    items = Transaction.objects.filter(user=request.user).select_related("category")
    kind = request.GET.get("type", "")
    search = request.GET.get("q", "").strip()
    if kind in ("income", "expense"):
        items = items.filter(kind=kind)
    if search:
        items = items.filter(title__icontains=search)
    return render(request, "tracker/transactions.html", {"transactions": items, "selected_type": kind, "search": search})

@login_required
def transaction_create(request):
    form = TransactionForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, "Transaction added successfully.")
        return redirect("transactions")
    return render(request, "tracker/transaction_form.html", {"form": form, "heading": "Add transaction"})

@login_required
def transaction_update(request, pk):
    item = get_object_or_404(Transaction, pk=pk, user=request.user)
    form = TransactionForm(request.POST or None, instance=item, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Transaction updated.")
        return redirect("transactions")
    return render(request, "tracker/transaction_form.html", {"form": form, "heading": "Edit transaction"})

@login_required
def transaction_delete(request, pk):
    item = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Transaction deleted.")
        return redirect("transactions")
    return render(request, "tracker/transaction_confirm_delete.html", {"transaction": item})

@login_required
def categories(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        try:
            category.save()
            messages.success(request, "Category created.")
            return redirect("categories")
        except Exception:
            form.add_error("name", "You already have a category with this name and type.")
    return render(request, "tracker/categories.html", {"form": form, "categories": Category.objects.filter(user=request.user)})

@login_required
def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="pennywise-transactions.csv"'
    writer = csv.writer(response)
    writer.writerow(["Date", "Title", "Type", "Category", "Amount", "Note"])
    for item in Transaction.objects.filter(user=request.user).select_related("category"):
        writer.writerow([item.date, item.title, item.kind, item.category.name if item.category else "", item.amount, item.note])
    return response
