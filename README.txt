django-date-extensions
by Matthew Somerville

This code adds a few small extensions to Django's DateField, to handle both
approximate dates (e.g. "March 1963") and default year dates (e.g. assume
"24th June" is the most recent such).

example contains a hopefully self-contained Django project that simply shows
off a form with these methods of entry.

Approximate dates
=================

A new object, ApproximateDate, is used to represent dates that might not have a
month or a day. ApproximateDateField is the model field used to represent these
objects in a Model, and ApproximateDateFormField is the field used in a Django
form. Everything should work seamlessly simply by specifying a model field as
ApproximateDateField rather than DateField.

Default year dates
==================

PrettyDateField is a form field to be used on DateField model fields. It takes
one argument, future, which is a nullable boolean. If True, a date input that
is missing a year will be taken to be the next possible occurrence of that date
- e.g. on 24th November 2009, entering 24th December will be taken to be
2009-12-24, whilst entering 3rd March will be taken to be 2010-03-03. If future
is False, the reverse occurs, with year-less dates being assumed to be the
closest occurrence of that date in the past.

If future is not set, then PrettyDateField acts the same as a DateField, only
allows suffixes on ordinals, and assumes D/M/Y rather than M/D/Y. 

Testing
=======
Run 'tox' with tox installed.

Todo
====

Improve date parsing to take more inputs like my traintimes.org.uk PHP, such as
"next Friday".


Any queries or comments, do get in touch. Something's probably broken, as I tried
to tidy up the code a little for public release :)

Matthew Somerville.
