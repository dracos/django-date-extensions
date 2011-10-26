import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'

from fields import ApproximateDate
import unittest


class CompareDates(unittest.TestCase):
    
    def test_compare(self):

        y_past     = ApproximateDate( year=2000 );
        y_future   = ApproximateDate( year=2100 );
        future     = ApproximateDate( future=True );

        # check that we can be compared to None, '' and u''
        for bad_val in ( '', u'', None ):
            self.assertFalse( y_past in ( bad_val, ) )
            self.assertFalse( y_past == bad_val      )
            self.assertTrue(  y_past != bad_val      )

        # sanity check
        self.assertTrue(  y_past   == y_past   )
        self.assertTrue(  y_future == y_future )

        self.assertFalse( y_past   != y_past   )
        self.assertFalse( y_future != y_future )

        self.assertTrue(  y_past   != y_future )
        self.assertTrue(  y_future != y_past   )

        self.assertTrue(  y_future >  y_past   )
        self.assertTrue(  y_future >= y_past   )
        self.assertFalse( y_past   >  y_future )
        self.assertFalse( y_past   >= y_future )

        self.assertTrue(  y_past   <  y_future )
        self.assertTrue(  y_past   <= y_future )
        self.assertFalse( y_future <  y_past   )
        self.assertFalse( y_future <= y_past   )

        # Future dates are always greater
        self.assertTrue( y_past   <  future )
        self.assertTrue( y_past   <= future )
        self.assertTrue( y_future <  future )
        self.assertTrue( y_future <= future )

        self.assertTrue( future >  y_past   )
        self.assertTrue( future >= y_past   )
        self.assertTrue( future >  y_future )
        self.assertTrue( future >= y_future )

        # Future dates are equal to themselves (so that sorting is sane)
        self.assertFalse( future <  future )
        self.assertTrue(  future <= future )
        self.assertTrue(  future == future )
        self.assertTrue(  future >= future )
        self.assertFalse( future >  future )


class Lengths(unittest.TestCase):
    known_lengths = (
        ({ 'year':1999,                        }, 10 ),
        ({ 'year':1999, 'month': 01,           }, 10 ),
        ({ 'year':1999, 'month': 01, 'day': 01 }, 10 ),
        ({ 'future': True },                      6  ),
    );
    
    def test_length(self):
        for kwargs, length in self.known_lengths:
            approx = ApproximateDate( **kwargs )
            self.assertEqual( len( approx ), length )

if __name__ == "__main__":
    unittest.main()   
