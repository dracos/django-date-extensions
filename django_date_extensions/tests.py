import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'

from fields import ApproximateDate
import unittest


class PastAndFuture(unittest.TestCase):

    def test_setting_both(self):
        self.assertRaises(ValueError, ApproximateDate, past=True, future=True )


    def test_setting_with_dates(self):
        self.assertRaises(ValueError, ApproximateDate, future=True, year=2000 )
        self.assertRaises(ValueError, ApproximateDate, past=True,   year=2000 )


    def test_stringification(self):

        self.assertEqual(str(ApproximateDate(future=True)), 'future')
        self.assertEqual(str(ApproximateDate(past=True)),   'past')

        self.assertEqual(repr(ApproximateDate(future=True)), 'future')
        self.assertEqual(repr(ApproximateDate(past=True)),   'past')


class CompareDates(unittest.TestCase):
    
    def test_compare(self):

        past       = ApproximateDate( past=True )
        past_too   = ApproximateDate( past=True )
        y_past     = ApproximateDate( year=2000 )
        y_future   = ApproximateDate( year=2100 )
        future     = ApproximateDate( future=True )
        future_too = ApproximateDate( future=True )

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
        self.assertTrue( y_past   != future )
        self.assertTrue( y_future <  future )
        self.assertTrue( y_future <= future )
        self.assertTrue( y_future != future )

        self.assertTrue( future >  y_past   )
        self.assertTrue( future >= y_past   )
        self.assertTrue( future != y_past   )
        self.assertTrue( future >  y_future )
        self.assertTrue( future >= y_future )
        self.assertTrue( future != y_future )

        # Past dates are always lesser
        self.assertTrue( y_past   >  past )
        self.assertTrue( y_past   >= past )
        self.assertTrue( y_past   != past )
        self.assertTrue( y_future >  past )
        self.assertTrue( y_future >= past )
        self.assertTrue( y_future != past )

        self.assertTrue( past <  y_past   )
        self.assertTrue( past <= y_past   )
        self.assertTrue( past != y_past   )
        self.assertTrue( past <  y_future )
        self.assertTrue( past <= y_future )
        self.assertTrue( past != y_future )
        

        # Past and future comparisons
        self.assertTrue( past   <  future )
        self.assertTrue( past   <= future )
        self.assertTrue( past   != future )

        self.assertTrue( future >  past   )
        self.assertTrue( future >= past   )
        self.assertTrue( future != past   )
        


        # Future and past dates are equal to themselves (so that sorting is sane)
        self.assertFalse( future <  future     )
        self.assertTrue(  future <= future     )
        self.assertTrue(  future == future     )
        self.assertTrue(  future >= future     )
        self.assertFalse( future >  future     )
        self.assertTrue(  future == future_too )
        self.assertFalse( future != future_too )

        self.assertFalse( past   <  past       )
        self.assertTrue(  past   <= past       )
        self.assertTrue(  past   == past       )
        self.assertTrue(  past   >= past       )
        self.assertFalse( past   >  past       )
        self.assertTrue(  past   == past_too   )
        self.assertFalse( past   != past_too   )

class Lengths(unittest.TestCase):
    known_lengths = (
        ({ 'year':1999,                        }, 10 ),
        ({ 'year':1999, 'month': 01,           }, 10 ),
        ({ 'year':1999, 'month': 01, 'day': 01 }, 10 ),
        ({ 'future': True },                      6  ),
        ({ 'past': True },                        4  ),
    );
    
    def test_length(self):
        for kwargs, length in self.known_lengths:
            approx = ApproximateDate( **kwargs )
            self.assertEqual( len( approx ), length )

if __name__ == "__main__":
    unittest.main()   
