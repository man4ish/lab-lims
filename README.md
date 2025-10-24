# lab-lims (Under development)

A lightweight Laboratory Information Management System (LIMS) built with Django to manage biological sample data, projects, and associated metadata.

## Overview

**lab-lims** is designed to help research teams track, organize, and search biological samples in a structured, user-friendly interface. It supports core LIMS features such as sample submission, metadata tracking, and secure access.

## Features

- Sample submission form with validation
- Models for Sample, Project, Organism, SampleType, SpecimenSource
- Email notifications on submission
- Authentication (planned)
- Role-based permissions (planned)
- CSV/Excel export
- Search and filter

## Tech Stack

- **Backend**: Django 5.2 (Python 3.12)
- **Database**: MySQL (configurable)
- **Frontend**: Bootstrap 5 (via templates)
- **Deployment**: (Planned) Heroku/DigitalOcean

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL (or SQLite for testing)
- pip

### Setup Instructions

1. Clone the repo:

   ```bash
   git clone https://github.com/man4ish/lab_data_manager.git
   cd lab_data_manager

2. Create virtual environment and install dependencies:

    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Apply migrations and run server:

    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
4. Open in browser: ```http://127.0.0.1:8000/core/samples/new/```

### Optional: Create superuser

```bash
python manage.py createsuperuser
```

### Project Structure

```bash
lab_data_manager/
├── core/
│   ├── models.py        # Sample, Project, etc.
│   ├── forms.py         # SampleForm
│   ├── views.py         # Form handling and success view
│   ├── urls.py          # App URL patterns
│   ├── templates/core/
│   │   ├── sample_form.html
│   │   └── sample_success.html
├── lab_data_manager/
│   ├── settings.py
│   ├── urls.py
├── manage.py
└── .gitignore
```

### Testing
```bash
python manage.py test
```
(Test coverage to be added.)

## CI/CD Integration

Continuous Integration and Deployment will be added using:

- **GitHub Actions** for automated testing and linting
- Optional **Docker support** for containerized deployment
- Deployment pipeline to platforms like Heroku, Render, or DigitalOcean (planned)

### Planned GitHub Actions Workflow

- Run unit tests on every push
- Check code style with flake8
- Auto-deploy to staging/production branch (optional)

### Example `.github/workflows/django.yml`

### Contact
For suggestions or questions, feel free to reach out at mandecent.gupta@gmail.com.
