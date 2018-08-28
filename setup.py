import os
from setuptools import setup



install_requires = [
    'beautifulsoup4==4.3.2',
    'Django>=1.8,<1.12',
    'dj-database-url==0.4.2',
    'python-dateutil==2.2',
    'requests==2.9.1',
    'six==1.9.0',
]


setup_requires=[
    'cfgov-setup==1.2',
    'setuptools-git-version==1.0.3',
]


testing_extras = [
    'coverage==4.2',
    'mock==1.0.1',
]


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='retirement',
    author='CFPB',
    author_email='tech@cfpb.gov',
    version_format='{tag}.dev{commitcount}+{gitsha}',
    maintainer='cfpb',
    maintainer_email='tech@cfpb.gov',
    packages=['retirement_api', 'retirement_api.utils'],
    include_package_data=True,
    description=u'Retirement app and api',
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.md'),
    zip_safe=False,
    install_requires=install_requires,
    setup_requires=setup_requires,
    extras_require={
        'testing': testing_extras,
    },
    frontend_build_script='frontendbuild.sh'
)
