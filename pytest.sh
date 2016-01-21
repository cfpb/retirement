#! /bin/bash
# run python unittests

export DJANGO_SETTINGS_MODULE=test_settings
coverage run --rcfile=.coveragerc --source='.' manage.py test
coverage report -m
