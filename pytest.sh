#! /bin/bash
# run python unittests

export DJANGO_SETTINGS_MODULE=test_settings
coverage run manage.py test > /dev/null
coverage report -m
