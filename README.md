# PennyWise — Expense Tracker

A personal finance dashboard built with Python, Django, SQLite, Bootstrap 5 and Chart.js.

## Features
- Secure registration, login and logout
- Private dashboard with income, expenses and balance summaries
- Create, edit and delete income/expense transactions
- Categories and transaction filtering
- Monthly spending chart and category breakdown
- CSV export of your transactions
- Responsive interface

## Quick start (Windows / VS Code)

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

## Project structure
- `config/` — Django project settings and URLs
- `tracker/` — transactions, categories, dashboard and authentication
- `templates/` — Bootstrap templates
- `static/` — custom CSS and JavaScript

## Notes
The app uses SQLite locally. Django creates `db.sqlite3` after migrations. Never commit secrets or your local database to a public repository.
