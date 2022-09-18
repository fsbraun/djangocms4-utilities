#!/usr/bin/env python
from setuptools import find_packages, setup

__version__ = "0.1.0"

REQUIREMENTS = [
    "Django>=2.2",
    "django-cms>=3.7",
]

setup(
    name="djangocms4-utilities",
    version=__version__,
    author="fsbraun",
    author_email="fsbraun@gmx.de",
    maintainer="Django CMS Association and contributors",
    maintainer_email="info@django-cms.org",
    url="https://github.com/fsbraun/djangocms4-utilities",
    license="BSD-3-Clause",
    description="Debugging utilites for django CMS V4",
    long_description=open("README.md").read(),
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
)
