import os
from setuptools import setup


install_requires = [
    "beautifulsoup4>=4.5.0,<4.9",
    "Django>=2.1,<3.2",
    "dj-database-url>=0.4.2,<1",
    "python-dateutil>=2.1,<3",
    "requests>=2.18,<3",
]


setup_requires = [
    "cfgov-setup==1.2",
    "setuptools-git-version==1.0.3",
]


testing_extras = [
    "coverage>=4.5.1,<5",
    "freezegun>=0.3.1,<1",
    "mock==2.0.0",
]


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ""


setup(
    name="retirement",
    author="CFPB",
    author_email="tech@cfpb.gov",
    version_format="{tag}.dev{commitcount}+{gitsha}",
    maintainer="cfpb",
    maintainer_email="tech@cfpb.gov",
    packages=["retirement_api", "retirement_api.utils"],
    include_package_data=True,
    description="Retirement app and api",
    classifiers=[
        "Topic :: Internet :: WWW/HTTP",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
    ],
    long_description=read_file("README.md"),
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=install_requires,
    setup_requires=setup_requires,
    extras_require={
        "testing": testing_extras,
    },
    frontend_build_script="frontendbuild.sh",
)
