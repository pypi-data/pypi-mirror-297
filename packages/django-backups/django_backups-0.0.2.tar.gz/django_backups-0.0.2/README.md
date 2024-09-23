# Django backups

A django backup package for backing up your databases.

## Installation

**NOTE**: Before installing this package, you should have postgresql installed on your machine.

Install through pip

```bash
pip install django-backups
```

In settings.py, add the following line:

```python
BACKUP_DIR = BASE_DIR / "backups_folder"
```

This is where your saved backups will go locally.

Add `backups` to INSTALLED_APPS.

```bash
INSTALLED_APPS = [
    ...

    'backups',
]
```

Add those two lines in settings.py:

```python
from dotenv import load_dotenv
load_dotenv()
```

Add the following lines to `.env` file:
```ini
DO_SPACE_ACCESS_KEY_ID='<key_id>'
DO_SPACE_SECRET_ACCESS_KEY='<secret_access_key>'
DO_SPACE_ENDPOINT_URL='<endpoint_url>'
DO_SPACE_BUCKET_NAME='<bucked_name>'
DO_SPACE_REGION='<s3_region>'
```

Include the urls in your `project/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('', include('backups.urls'))
]
```

**NOTE**: Don't worry about `DO_SPACE`, it'll work with S3 in general.

Before running the server, make sure to do `python manage.py migrate`

# Integration with Celery

By default, if you've already installed celery in your project, the tasks will be load to Celery, just make sure it's up and running.

# TODO

- [ ] store credentials for Servers and tables.
- [ ] Actions for:
    1. Servers:
        - Check server connection (even before storing server info).
        - Get server databases and store them
        - Backup all databases.
    2. Databases:
        - Update all tables
        - Backup database.

- [ ] Backup:
    - Upload to S3.
    - Store backup locally on server
    - Download backup file from server.
