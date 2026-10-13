# swe1-app

A Django 5.2 polls app following tutorial parts 1–4: browse published polls,
vote, see results, and manage questions and choices in Django admin.

## Run locally

Requires Python 3.10 or newer.

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

Open http://127.0.0.1:8000/polls/. Create an admin user with
python manage.py createsuperuser, then visit /admin/ to add questions and choices.

## Deploy to AWS Elastic Beanstalk

Install and configure the AWS CLI and EB CLI with credentials for your own AWS
account. From this directory, choose your AWS region and run:

    eb init -p python-3.12 swe1-app --region YOUR_AWS_REGION
    eb create swe1-app-env
    eb setenv DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" DJANGO_ALLOWED_HOSTS=".elasticbeanstalk.com"
    eb deploy
    eb status

Use the CNAME shown by eb status as the application URL; append /polls/.
The first deployment runs database migrations. The included SQLite database is
ephemeral on Elastic Beanstalk instances; use a managed database such as Amazon
RDS if poll data must persist across instance replacement or scaling.
