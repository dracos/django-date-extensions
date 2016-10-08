from setuptools import setup

setup(
    name='django_date_extensions',
    version='2.0',
    url='https://github.com/dracos/django-date-extensions',
    packages=['django_date_extensions',],
    license='BSD',
    description="This code adds a few small extensions to Django's DateField, to handle both approximate dates (e.g. 'March 1963') and default year dates (e.g. assume '24th June' is the most recent such).",
    long_description=open('README.txt').read(),
    author='Matthew Somerville',
    author_email='matthew-pypi@dracos.co.uk',
    requires=[
        'Django',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
