# Contributing to vet-software

This guide covers the complete development workflow for the vet-software project, from initial setup to deployment. Follow these guidelines to ensure consistency across the team.

## Table of Contents

- [Contributing to vet-software](#contributing-to-vet-software)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [VS Code Setup](#vs-code-setup)
  - [Getting Started](#getting-started)
  - [Development Workflow](#development-workflow)
  - [Commit Message Conventions](#commit-message-conventions)
  - [Creating a New Django App](#creating-a-new-django-app)
  - [Working with Django Models](#working-with-django-models)
  - [Working with Tailwind CSS](#working-with-tailwind-css)
  - [Populating Database with Dummy Data](#populating-database-with-dummy-data)
  - [Testing](#testing)
  - [Make an SQL dump](#make-an-sql-dump)

## Prerequisites

- **Python 3.10+**
- **Node.js 20.x LTS or higher** (for Tailwind CSS compilation)
- **Git**
- **Virtual environment tool** (venv)
- **VS Code** (recommended)

---

## VS Code Setup

To ensure consistent code formatting across the team, install the following VS Code extensions:

### Required Extensions

1. **Better Jinja** (`samuelcolvin.jinjahtml`)

2. **Black Formatter** (`ms-python.black-formatter`)

3. **djLint** (`monosans.djlint`)

### Installation

```bash
# Open VS Code
# Press Ctrl+Shift+X (on Windows/Linux)
# Search for and install:
# - Better Jinja
# - Black Formatter
# - djLint
```

### Settings

The project includes a `.vscode/settings.json` file:

---

## Getting Started

### Initial Setup

1. **Clone the repository**

```bash
git clone https://github.com/relka-dev/vet-software.git
cd vet-software
```

2. **Create and activate virtual environment**

_Linux/Mac OS:_

```bash
python -m venv venv
source venv/bin/activate
```

_Windows:_

```powershell
python -m venv venv
venv\Scripts\activate
```

3. **Install dependencies**

```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (for Tailwind)
cd static
npm install
cd ..
```

4. **Setup Django**

```bash
cd src
python manage.py migrate
python manage.py createsuperuser
```

5. **Populate database with dummy data**

```bash
# Populate all apps at once (recommended)
python manage.py populate_all

# Or populate individual apps in order
python manage.py populate_person
python manage.py populate_family
python manage.py populate_employee
python manage.py populate_animal
python manage.py populate_inventory
python manage.py populate_appointment
```

6. **Run development servers**

_Terminal 1 - Tailwind CSS (keep running):_

```bash
cd static
npx tailwindcss -i ./src/input.css -o ./src/output.css --watch
```

_Terminal 2 - Django:_

```bash
cd src
python manage.py runserver
```

7. **Access the application**

- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

---

## Development Workflow

We use the [**Feature Branch Workflow**](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).

### Branch Strategy

- **`main`**: Production-ready code, always stable
- **`feature/*`**: New features (e.g., `feature/appointment-booking`)
- **`hotfix/*`**: Urgent bug fixes (e.g., `hotfix/login-error`)

### Workflow Steps

#### 1. Start a new feature

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

#### 2. Develop and commit

```bash
git add .
git commit -m "Code: Add appointment model"
```

#### 3. Keep branch updated

```bash
git checkout main
git pull origin main
git checkout feature/your-feature-name
git merge main
```

#### 4. Push and create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:

- Clear title describing the feature
- Description of changes and why they're needed
- At least one reviewer assigned

#### 5. After PR approval

```bash
# Merge on GitHub, then locally:
git checkout main
git pull origin main
git branch -d feature/your-feature-name
```

---

## Commit Message Conventions

Always prefix commits with one of these:

| Prefix | Domain           | Description                                            |
| ------ | ---------------- | ------------------------------------------------------ |
| Code   | Code / Features  | Code implementation and functionality                  |
| Docs   | Documentation    | Documentation / Project readability (ReadMe, etc.)     |
| Struct | Structure        | Project structure                                      |
| Mixed  | Multiple domains | Multiple domains changed (detailed description needed) |
| Hotfix | Quick fix        | Quick modification to repair an error or bug           |

**Examples:**

```bash
git commit -m "Code: Add appointment booking feature"
git commit -m "Docs: Update installation instructions"
git commit -m "Struct: Reorganize app modules"
git commit -m "Hotfix: Fix null pointer exception in appointment view"
```

---

## Creating a New Django App

Follow these steps to create and integrate a new app into the project:

### Step 1: Create the app

```bash
cd src
python manage.py startapp app_name
```

**Example:** `python manage.py startapp appointments`

### Step 2: Register the app in settings

Add your app to `INSTALLED_APPS` in `src/vet_software/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'app_name',  # Add your new app here
]
```

### Step 3: Define models

Create your models in `src/app_name/models.py`:

```python
from django.db import models

class YourModel(models.Model):
    """Description of your model"""

    name = models.CharField(
        max_length=100,
        verbose_name="Name"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )

    class Meta:
        verbose_name = "Your Model"
        verbose_name_plural = "Your Models"
        ordering = ['name']

    def __str__(self):
        return self.name
```

**Key points:**

- Always use `verbose_name` for fields
- Include `class Meta` with verbose names
- Implement `__str__()` method
- Use `ForeignKey` for relations (not `IntegerField`)

### Step 4: Create and apply migrations

```bash
cd src

# Create migrations
python manage.py makemigrations app_name

# Review the migration (optional)
python manage.py sqlmigrate app_name 0001

# Apply migrations
python manage.py migrate
```

### Step 5: Register models in admin

Edit `src/app_name/admin.py`:

```python
from django.contrib import admin
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    ordering = ['name']
```

### Step 6: Create URLs (if needed)

Create `src/app_name/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='app_name_index'),
]
```

Add to main `src/vet_software/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('app_name/', include('app_name.urls')),  # Add this
]
```

### Step 7: Create views (if needed)

Edit `src/app_name/views.py`:

```python
from django.shortcuts import render
from .models import YourModel

def index(request):
    items = YourModel.objects.all()
    return render(request, 'app_name/index.html', {'items': items})
```

### Step 8: Create templates (if needed)

Create directory structure:

```bash
mkdir -p src/app_name/templates/app_name
```

Create `src/app_name/templates/app_name/index.html`:

```html
{% load static %}
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>App Name</title>
    <link rel="stylesheet" href="{% static 'output.css' %}" />
  </head>
  <body>
    <h1>Your App</h1>
    {% for item in items %}
    <p>{{ item.name }}</p>
    {% endfor %}
  </body>
</html>
```

### Step 9: Test your app

```bash
cd src
python manage.py runserver
```

Visit:

- Admin: http://127.0.0.1:8000/admin/ (to manage data)
- Your app: http://127.0.0.1:8000/app_name/ (if you created views/URLs)

### Step 10: Commit your work

```bash
git add .
git commit -m "Code: Add app_name app with YourModel"
git push origin feature/your-feature-name
```

---

## Working with Django Models

### Model Relationships

**ForeignKey (Many-to-One):**

```python
class Animal(models.Model):
    owner = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,  # Delete animal if client is deleted
        related_name='animals',
        verbose_name="Owner"
    )
```

**OneToOneField (One-to-One):**

```python
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
```

**ManyToManyField (Many-to-Many):**

```python
class Appointment(models.Model):
    procedures = models.ManyToManyField(
        Procedure,
        through='AppointmentProcedure',  # With intermediate table
        related_name='appointments'
    )
```

### on_delete Options

- `CASCADE`: Delete related objects
- `PROTECT`: Prevent deletion if related objects exist
- `SET_NULL`: Set to NULL (requires `null=True`)
- `SET_DEFAULT`: Set to default value (requires `default=...`)

### Before Pushing Changes

```bash
# Check for migration issues
python manage.py makemigrations --check --dry-run

# Run tests (if available)
python manage.py test

# Test the server
python manage.py runserver
```

---

## Working with Tailwind CSS

### Development

Keep this running while developing:

```bash
cd static
npm run watch
```

### Custom Styles

- Edit `static/src/input.css` for custom CSS
- Use Tailwind utility classes in templates whenever possible
- Only add custom CSS when Tailwind utilities are insufficient

---

## Populating Database with Dummy Data

The project includes management commands to populate the database with test data.

### Quick Start

To populate all data at once:

```bash
cd src
python manage.py populate_all
```

This will:

1. Clear all existing data (in the correct order to avoid foreign key conflicts)
2. Create persons, families, employees, animals, inventory items, and appointments
3. Display a summary of created data

### Individual Commands

You can also populate each app separately (must be run in this order):

```bash
# 1. Create persons (base data)
python manage.py populate_person

# 2. Create families (depends on persons)
python manage.py populate_family

# 3. Create employees (depends on persons)
python manage.py populate_employee

# 4. Create animals (depends on families)
python manage.py populate_animal

# 5. Create inventory items
python manage.py populate_inventory

# 6. Create appointments (depends on animals, employees, inventory)
python manage.py populate_appointment
```

### Creating Your Own Populate Command

When creating a new app, you should add a populate command:

1. **Create the directory structure:**

```bash
mkdir -p src/your_app/management/commands
touch src/your_app/management/__init__.py
touch src/your_app/management/commands/__init__.py
```

2. **Create the populate command:**

Create `src/your_app/management/commands/populate_your_app.py`:

```python
from django.core.management.base import BaseCommand
from your_app.models import YourModel

class Command(BaseCommand):
    help = 'Populate your_app data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating your_app data...")

        # Create your test data
        obj1 = YourModel.objects.create(
            name="Test Object 1",
            # ... other fields
        )

        obj2 = YourModel.objects.create(
            name="Test Object 2",
            # ... other fields
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {YourModel.objects.count()} objects"
            )
        )
```

3. **Add to populate_all:**

Update `src/home/management/commands/populate_all.py` to include your new command in the appropriate position based on dependencies.

---

## Testing

### Run Tests

```bash
cd src
python manage.py test
```

### Writing Tests

Create tests in `app_name/tests.py`:

```python
from django.test import TestCase
from .models import YourModel

class YourModelTest(TestCase):
    def setUp(self):
        """Create test data"""
        self.obj = YourModel.objects.create(name="Test")

    def test_model_creation(self):
        """Test object creation"""
        self.assertEqual(self.obj.name, "Test")

    def test_str_method(self):
        """Test string representation"""
        self.assertEqual(str(self.obj), "Test")
```

---

## Make an SQL dump

_Linux/Mac OS:_

```bash
cd src
sqlite3 db.sqlite3 ".dump" > ../db/dump-$(date +%d.%m.%Y).sql
```

_Windows_

```sh
cd src
sqlite3 db.sqlite3 ".dump" > ..\db\dump-%date:~0,2%.%date:~3,2%.%date:~6,4%.sql
```
