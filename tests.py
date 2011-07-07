import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'

from fields import ApproximateDate
import unittest


class Lengths(unittest.TestCase):
    known_lengths = (
        ({ 'year':1999,                        }, 10 ),
        ({ 'year':1999, 'month': 01,           }, 10 ),
        ({ 'year':1999, 'month': 01, 'day': 01 }, 10 ),
    );
    
    def test_length(self):
        for kwargs, length in self.known_lengths:
            print kwargs
            approx = ApproximateDate( **kwargs )
            self.assertEqual( len( approx ), length )

if __name__ == "__main__":
    unittest.main()   
