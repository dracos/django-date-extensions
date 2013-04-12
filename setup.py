from distutils.core import setup

setup(
    name='django_date_extensions',
    version='0.1dev',
    url='https://github.com/dracos/django-date-extensions',
    packages=['django_date_extensions',],
    license='GNU Affero General Public license',
    description="This code adds a few small extensions to Django's DateField, to handle both approximate dates (e.g. 'March 1963') and default year dates (e.g. assume '24th June' is the most recent such).",
    long_description=open('README.txt').read(),
    author='Matthew Somerville',
    author_email='matthew-pypi@dracos.co.uk',
    requires=[ 'Django' ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
