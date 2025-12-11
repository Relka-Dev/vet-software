# Contributing

### Prerequisites

- **Python 3.10+**
- **Node.js 20.x LTS or higher** (for Tailwind CSS compilation)
- **Git**
- **Virtual environment tool** (venv) or other if the packages are compatible

### Getting started, initial Setup

1. **Clone the repository**

_Start by making sure to have the correct access rights. For any questions, please contact : <relka.dev@gmail.com>_

```bash
git clone https://github.com/relka-dev/vet-software.git
cd vet-software
```

2. **Create and activate virtual environment**

_On Linux or Mac OS_

```bash
python -m venv venv
source venv/bin/activate
```

_On Windows_

```powershell
python -m venv venv
venv\Scripts\activate
```

3. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

4. **Install Node.js dependencies (for Tailwind CSS)**

```bash
cd static
npm install
cd ..
```

5. **Apply database migrations**

```bash
cd src
python manage.py migrate
```

6. **Create a superuser (optional, for admin access)**

```bash
python manage.py createsuperuser
```

7. **Compile Tailwind CSS (in a separate terminal)**

_Keep this running during development for automatic CSS compilation_

```bash
cd static
npx tailwindcss -i ./src/input.css -o ./src/output.css --watch
```

8. **Run the development server (in another terminal)**

```bash
cd src
python manage.py runserver
```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

### Contributing

We use the [**Feature Branch Workflow**](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).

- **`main`**: Production-ready code, always stable
- **`feature/*`**: New features
- **`hotfix/*`**: Urgent bug fixes

#### 1. Start a new feature

```bash
# Update your local main branch
git checkout main
git pull origin main

# Create a new feature branch
git checkout -b feature/your-feature-name
```

#### 2. Develop your feature

```bash
# Make changes to your code
git add .
git commit -m "Code: Add appointment model"
```

⚠️ To Complete ⚠️

## Push normalisation

| Prefix | Domain           | Description                                                 |
| ------ | ---------------- | ----------------------------------------------------------- |
| Code   | Code / Features  | Code implementation and functionality                       |
| Docs   | Documentation    | Documentation / Project readability (ReadMe, etc.)          |
| Struct | Structure        | Project structure                                           |
| Mixed  | Multiple domains | Multiple domains changed (Detailed description recommended) |
| Hotfix | Quick fix        | Quick modification to repair an error or bug                |
