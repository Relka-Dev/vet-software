# Contributing

### Prerequisites

- Python 3.10+
- Git
- Virtual environment tool (venv) or other if the packages are compatible

### Getting started, initial Setup

1. **Clone the repository**

*Start by making sure to have the correct access rights. For any questions, please contact : <relka.dev@gmail.com>*

```bash
   git clone https://github.com/relka-dev/vet-software.git
   cd vet-software
   cd src # Go to the project source
```

1. **Create and activate virtual environment**

*On Linux or Mac OS*

```bash
python -m venv venv
source venv/bin/activate
```

*On Windows*

```sh
python -m venv venv
venv\Scripts\activate  
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply database migrations**
```bash
python manage.py migrate
```


5. **Create a superuser (optional, for admin access)**
```bash
   python manage.py createsuperuser
```


6. **Run the development server**
```bash
   python manage.py runserver
```

7. **Access the application**
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

| Prefix  | Domain            | Description                                              |
|---------|-------------------|----------------------------------------------------------|
| Code    | Code / Features   | Code implementation and functionality                    |
| Docs    | Documentation     | Documentation / Project readability (ReadMe, etc.)       |
| Struct  | Structure         | Project structure                                        |
| Mixed   | Multiple domains  | Multiple domains changed (Detailed description recommended) |
| Hotfix  | Quick fix         | Quick modification to repair an error or bug             | 