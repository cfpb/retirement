 [![Build Status](https://travis-ci.org/cfpb/retirement.png)](https://travis-ci.org/cfpb/retirement) [![Coverage Status](https://coveralls.io/repos/cfpb/retirement/badge.svg)](https://coveralls.io/r/cfpb/retirement)

# Retirement: Claiming Social Security

This is a project aimed at helping Americans make choices about retirement, including when to claim Social Security benefits.   
  - **Status**: Beta

### Setup dependencies
 * [pip](https://pypi.python.org/pypi/pip)
 * [virtualenv](https://virtualenv.pypa.io/en/latest/)
 * [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)

### Code dependencies 
 * [Django 1.6.11](https://docs.djangoproject.com/en/1.6/)
 * [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
 * [Python-dateutil](https://dateutil.readthedocs.org/en/latest/)
 * [Requests](http://docs.python-requests.org/en/latest/)
 * [lxml](http://lxml.de/installation.html)

### For testing
 * [nose](https://nose.readthedocs.org/en/latest/)
 * [mock](https://mock.readthedocs.org/en/latest/)
 * [coverage](http://nedbatchelder.com/code/coverage/)
 
<!--
 * [Homebrew](http://brew.sh)
 * [Django localflavor](https://github.com/django/django-localflavor)
 * [Django Rest Framework](http://www.django-rest-framework.org)
 * [MySQL Python](http://mysql-python.sourceforge.net/)
 * [South](http://south.aeracode.org)
 * [django-cors-headers](https://github.com/ottoyiu/django-cors-headers)
-->

### Installation
The tool is a Django module, intended to be installed and run inside a larger Django project. But you can run it as its own project for testing by copying the test_settings.py file as settings.py

These instructons assume a Mac or Linux environment with pip, virtualenv and virtualenvwrapper installed.

<!--[Homebrew](http://brew.sh) -->

Go to where you want the project to be created, make a virtual environment, clone this repository (or, better yet, your own fork of it) and install requirements and settings.
```bash
mkvirtualenv retirement
git clone https://github.com/cfpb/retirement.git
cd retirement
setvirtualenvproject
pip install -r requirements.txt
cp test_settings.py settings.py
```

Load the app's database tables and content.  
```bash
python manage.py syncdb
python manage.py loaddata retiredata.json
```

Fire up a development server to see if everything's working.
```bash
python manage.py runserver
```

The "Claiming Social Security" page should load at `localhost:8000/claiming-social-security/`.  

### Usage notes
- The app is set up to run inside [consumerfinance.gov](http://www.consumerfinance.gov), so if you run it locally, some fonts may not load because of Cross-Origin Resource Sharing rules.
- The app sends http requests to the Social Security Administration's [Quick Calculator](http://www.ssa.gov/OACT/quickcalc/index.html) to get benefit estimates for the chart. 

### How to run software tests
- You can use nose to run the test suite and see code coverage information
```bash
nosetests --with-coverage --config=.coveragerc --cover-package retirement_api/utils
```

## Getting involved
If you find a bug or see a way to improve the project, we'd love to hear from you. Fork the project and send us a pull request with your changes.

----

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


----
