# 🐾 Vet Software

A comprehensive veterinary clinic management system to streamline the entire workflow of a vet clinic.

## Project Overview

This system helps veterinary clinics manage appointments, patient records, treatments, and administrative tasks efficiently.

## Tech Stack

- **Backend**: Django 6.0 (Python)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: Tailwind CSS 3.x + Flowbite
- **Testing**: pytest, pytest-django, pytest-cov
- **Build Tools**: Node.js, npm

## Quick Start

For detailed installation and setup instructions, please see [CONTRIBUTING.md](CONTRIBUTING.md).

**Prerequisites**: Python 3.10+, Node.js 20.x LTS, Git

**Quick access after setup**:

- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Sending Reminder Emails

The system can automatically send reminder emails to staff for items that need follow-ups (e.g., 30 days after an appointment).

### Prerequisites

Configure your email settings in `.env` file:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Sending Reminders

Run the command to send reminder emails for today's reminders:

```bash
python manage.py send_reminder_emails
```

## Project Structure

```
vet-software/
├── src/                   # Django project source
│   ├── app_name/          # Main application (for each modules)
│   │   ├── templates/     # HTML templates
│   │   ├── views.py       # View functions
│   │   └── urls.py        # URL routing
│   │   └── models.py      # DataBase Tables
│   │   └── forms.py       # User inputs
│   ├── vet_software/      # Project settings
│   │   └── settings.py    # Django configuration
│   └── manage.py          # Django management script
├── static/                # Static assets
│   ├── src/
│   │   ├── input.css      # Tailwind source
│   │   └── output.css     # Compiled CSS (generated)
│   └── tailwind.config.js # Tailwind configuration
├── docs/                  # Documentation
├── venv/                  # Virtual environment
└── requirements.txt       # Python dependencies

```

## SQL SCHEMA

[DB Schema Link](https://dbdiagram.io/d/Copy-of-genie-logiciel-6964d8c5d6e030a024c4eeb1)

<img width="2240" height="1288" alt="ERD_SCHEMA_2026_01_12" src="https://github.com/user-attachments/assets/89a977b2-0dec-452d-80f5-34ac1d7d7553" />

**SQL dumps :** can be found [here](./db).

## SCREENSHOTS

**Home Page**
<img width="1918" height="877" alt="acceuil" src="https://github.com/user-attachments/assets/b944110c-a378-470a-926a-a18f0591dae8" />

**Login Page**
<img width="1918" height="878" alt="login" src="https://github.com/user-attachments/assets/dbb596c8-2a17-4e48-9107-63d116dd8194" />

**Calandar and add an appointment**
<img width="1917" height="880" alt="add_appointment_calandar" src="https://github.com/user-attachments/assets/918649af-525f-42ec-9bc5-2209b3f218d9" />

**Reminder Page**
<img width="1919" height="879" alt="reminders" src="https://github.com/user-attachments/assets/bbb4a85c-01de-411f-adf8-4d8bbfa9516a" />

**SOAP Note Page**
<img width="1918" height="881" alt="SOAPNote" src="https://github.com/user-attachments/assets/6980172c-8972-4a83-8b6e-57ecf81eb929" />

**Family Page**
<img width="1918" height="878" alt="family" src="https://github.com/user-attachments/assets/32a0d2cd-d92c-4b98-a913-56bd552cbfc6" />

**DashBoard View**
<img width="1919" height="877" alt="dashboard" src="https://github.com/user-attachments/assets/df30963a-f408-471f-8f28-2db373086a2e" />

**Logs View**
<img width="1918" height="875" alt="logs" src="https://github.com/user-attachments/assets/1bceb7a6-b49b-4568-b470-53a0b92d3dc8" />

## Authors

**Aurélie Pham** • **Grace Naing** • **Karel Vilém Svoboda**

**Affiliation**: HES-SO Valais / Wallis (2025-2026)

**Courses**: 201.2 Génie logiciel • 201.3 BD relationnelles

## License

See [LICENSE](LICENSE) file for details.
