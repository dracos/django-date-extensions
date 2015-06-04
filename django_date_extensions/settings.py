from django.conf import settings

OUTPUT_FORMAT_DAY_MONTH_YEAR = getattr(settings, 'DATE_EXTENSIONS_OUTPUT_FORMAT_DAY_MONTH_YEAR', "jS F Y")

OUTPUT_FORMAT_MONTH_YEAR = getattr(settings, 'DATE_EXTENSIONS_OUTPUT_FORMAT_MONTH_YEAR', "F Y")

OUTPUT_FORMAT_YEAR = getattr(settings, 'DATE_EXTENSIONS_OUTPUT_FORMAT_YEAR', "Y")

# The same as the built-in Django one, but with the d/m/y ones the right way round ;)
DATE_INPUT_FORMATS = getattr(settings, 'DATE_EXTENSIONS_DATE_INPUT_FORMATS', (
    '%Y-%m-%d',  # '2006-10-25',
    '%d/%m/%Y', '%d/%m/%y',  # '25/10/2006', '25/10/06'
    '%b %d %Y', '%b %d, %Y',  # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',  # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
))

MONTH_INPUT_FORMATS = getattr(settings, 'DATE_EXTENSIONS_MONTH_INPUT_FORMATS', (
    '%m/%Y', '%m-%Y',  # '10/2006', '10-2006'
    '%b %Y', '%Y %b',  # 'Oct 2006', '2006 Oct'
    '%B %Y', '%Y %B',  # 'October 2006', '2006 October'
))

YEAR_INPUT_FORMATS = getattr(settings, 'DATE_EXTENSIONS_YEAR_INPUT_FORMATS', (
    '%Y',  # '2006'
))

DAY_MONTH_INPUT_FORMATS = getattr(settings, 'DATE_EXTENSIONS_DAY_MONTH_INPUT_FORMATS', (
    '%m-%d', '%d/%m',  # '10-25', '25/10'
    '%b %d', '%d %b',  # 'Oct 25', '25 Oct'
    '%B %d', '%d %B',  # 'October 25', '25 October'
))
