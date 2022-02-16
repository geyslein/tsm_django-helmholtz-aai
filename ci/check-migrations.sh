#!/bin/sh
# Test if the migrations are up-to-date for tags, and otherwise, make them

set -e

case $CI_COMMIT_TAG in
    "")
        python manage.py makemigrations;;
    *)
        python manage.py makemigrations;;
esac
