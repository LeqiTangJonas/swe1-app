# swe1-app

[![Build Status](https://app.travis-ci.com/LeqiTangJonas/swe1-app.svg?branch=main)](https://app.travis-ci.com/github/LeqiTangJonas/swe1-app)
[![Coverage Status](https://coveralls.io/repos/github/LeqiTangJonas/swe1-app/badge.svg?branch=main)](https://coveralls.io/github/LeqiTangJonas/swe1-app?branch=main)

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

## Continuous integration

Travis CI runs Black, Flake8, and the Django test suite with Coverage.py on pushes
and pull requests. Successful pushes to `main` deploy to the Elastic Beanstalk
environment. Pull request builds run checks but do not deploy.

Install the development tools and run the same checks locally:

    python -m pip install -r requirements-dev.txt
    black --check .
    flake8 .
    coverage run manage.py test
    coverage report

Travis requires repository environment variables `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, and `COVERALLS_REPO_TOKEN`. Store these in the Travis
repository settings; never commit credentials to this repository. Use a dedicated
IAM identity for deployment credentials, not AWS root credentials.

Travis dashboard: https://app.travis-ci.com/github/LeqiTangJonas/swe1-app

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
