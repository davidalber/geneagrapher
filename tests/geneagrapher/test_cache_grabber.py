import os
from time import time
import unittest
from local_data_grabber import LocalDataGrabber
from geneagrapher.cache_grabber import CacheGrabber
from geneagrapher.grabber import Grabber


class TestCacheGrabberMethods(unittest.TestCase):
    """Unit tests for the geneagrapher.CacheGrabber class."""
    def setUp(self):
        self.name = u"Carl Friedrich Gau\xdf"
        self.institution = u"Universit\xe4t Helmstedt"
        self.year = 1799
        self.advisors = set([18230])
        self.descendants = set([18603, 18233, 62547, 29642, 55175,
                                29458, 19953, 18232, 151876])

    def tearDown(self):
        try:
            os.remove('geneacache')
        except OSError:
            pass

    def test_init1(self):
        """Test constructor."""
        cache = CacheGrabber()
        self.assertEqual(cache.filename, 'geneacache')
        self.assertEqual(len(cache.cache), 0)
        self.assertIsInstance(cache.grabber, Grabber)
        self.assertEqual(cache.expiration_interval, 604800.)

    def test_init2(self):
        """Test constructor with non-default filename."""
        cache = CacheGrabber('mycachename')
        self.assertEqual(cache.filename, 'mycachename')
        self.assertEqual(len(cache.cache), 0)
        self.assertIsInstance(cache.grabber, Grabber)
        self.assertEqual(cache.expiration_interval, 604800.)
        os.remove('mycachename')

    def test_init3(self):
        """Test constructor with non-default record grabber."""
        cache = CacheGrabber(record_grabber=LocalDataGrabber)
        self.assertEqual(cache.filename, 'geneacache')
        self.assertEqual(len(cache.cache), 0)
        self.assertIsInstance(cache.grabber, LocalDataGrabber)
        self.assertEqual(cache.expiration_interval, 604800.)

    def test_init4(self):
        """Test constructor with non-default expiration interval."""
        cache = CacheGrabber(expiration_interval=1209600.)
        self.assertEqual(cache.filename, 'geneacache')
        self.assertEqual(len(cache.cache), 0)
        self.assertIsInstance(cache.grabber, Grabber)
        self.assertEqual(cache.expiration_interval, 1209600.)

    def test_close(self):
        """Test the close method."""
        cache = CacheGrabber(record_grabber=LocalDataGrabber)
        self.assertEqual(len(cache.cache), 0)
        cache.close()
        self.assertRaisesRegexp(ValueError,
                                'invalid operation on closed shelf',
                                len, cache.cache)

    def test_is_expired_false(self):
        """Test the is_expired method."""
        t = time()
        d = {'name': self.name, 'institution': self.institution,
             'year': self.year, 'advisors': self.advisors,
             'descendants': self.descendants, 'timestamp': t}
        with CacheGrabber() as cache:
            self.assertFalse(cache.is_expired(d))
            d['timestamp'] = time() - cache.expiration_interval + 20
            self.assertFalse(cache.is_expired(d))

    def test_is_expired_true(self):
        """Test the is_expired method."""
        with CacheGrabber() as cache:
            t = time() - cache.expiration_interval - 1
            d = {'name': self.name, 'institution': self.institution,
                 'year': self.year, 'advisors': self.advisors,
                 'descendants': self.descendants, 'timestamp': t}
            self.assertTrue(cache.is_expired(d))

    def test_context_manager(self):
        """Test the context manager methods."""
        with CacheGrabber(record_grabber=LocalDataGrabber) as cache:
            self.assertEqual(len(cache.cache), 0)
        self.assertRaisesRegexp(ValueError,
                                'invalid operation on closed shelf',
                                len, cache.cache)

    def test_get_record_bad(self):
        """Test the get_record method for a bad id."""
        with CacheGrabber(record_grabber=LocalDataGrabber) as cache:
            self.assertEqual(len(cache.cache), 0)
            self.assertRaisesRegexp(ValueError, 'Invalid id 999999999',
                                    cache.get_record, 999999999)
            self.assertEqual(len(cache.cache), 0)

    def test_get_record(self):
        """Test the get_record method for a good id."""
        with CacheGrabber(record_grabber=LocalDataGrabber) as cache:
            record = cache.get_record(18231)
            self.assertEqual(len(record), 6)
            self.assertEqual(record['name'], u"Carl Friedrich Gau\xdf")
            self.assertEqual(record['institution'],
                             u"Universit\xe4t Helmstedt")
            self.assertEqual(record['year'], 1799)
            self.assertEqual(record['advisors'], set([18230]))
            self.assertEqual(record['descendants'],  set([234500, 234374, 55175,
                                                          151876, 29642, 18603,
                                                          19953, 217618, 62547,
                                                          225908, 166471, 18232,
                                                          18233, 234267,
                                                          165758]))
            self.assertEqual(record['message'], u"cache miss")
            self.assertEqual(len(cache.cache), 1)

            # Make the request again and verify the cached version is returned.
            d = cache.cache['18231']
            d['institution'] = u'Rigged for test'
            cache.cache['18231'] = d
            record = cache.get_record(18231)
            self.assertEqual(len(record), 6)
            self.assertEqual(record['name'], u"Carl Friedrich Gau\xdf")
            self.assertEqual(record['institution'], u"Rigged for test")
            self.assertEqual(record['year'], 1799)
            self.assertEqual(record['advisors'], set([18230]))
            self.assertEqual(record['descendants'], set([234500, 234374, 55175,
                                                         151876, 29642, 18603,
                                                         19953, 217618, 62547,
                                                         225908, 166471, 18232,
                                                         18233, 234267,
                                                         165758]))
            self.assertEqual(record['message'], u"cache hit")
            self.assertEqual(len(cache.cache), 1)

        with CacheGrabber(record_grabber=LocalDataGrabber) as cache:
            # Redo the last request, this time with a newly-loaded instance
            # of the cache from disk.
            self.assertEqual(len(cache.cache), 1)
            d = cache.cache['18231']
            d['institution'] = u'Rigged for test'
            cache.cache['18231'] = d
            record = cache.get_record(18231)
            self.assertEqual(len(record), 6)
            self.assertEqual(record['name'], u"Carl Friedrich Gau\xdf")
            self.assertEqual(record['institution'], u"Rigged for test")
            self.assertEqual(record['year'], 1799)
            self.assertEqual(record['advisors'], set([18230]))
            self.assertEqual(record['descendants'], set([234500, 234374, 55175,
                                                         151876, 29642, 18603,
                                                         19953, 217618, 62547,
                                                         225908, 166471, 18232,
                                                         18233, 234267,
                                                         165758]))
            self.assertEqual(record['message'], u"cache hit")
            self.assertEqual(len(cache.cache), 1)

            # Make another request, this time with the cached entry expired,
            # and verify a new version is retrieved.
            d['timestamp'] = time() - cache.expiration_interval - 1
            cache.cache['18231'] = d
            record = cache.get_record(18231)
            self.assertEqual(len(record), 6)
            self.assertEqual(record['name'], u"Carl Friedrich Gau\xdf")
            self.assertEqual(record['institution'],
                             u"Universit\xe4t Helmstedt")
            self.assertEqual(record['year'], 1799)
            self.assertEqual(record['advisors'], set([18230]))
            self.assertEqual(record['descendants'], set([234500, 234374, 55175,
                                                         151876, 29642, 18603,
                                                         19953, 217618, 62547,
                                                         225908, 166471, 18232,
                                                         18233, 234267,
                                                         165758]))
            self.assertEqual(record['message'], u"cache miss")
            self.assertEqual(len(cache.cache), 1)

    def test_is_in_cache(self):
        """Test the is_in_cache method."""
        d = {'name': self.name, 'institution': self.institution,
             'year': self.year, 'advisors': self.advisors,
             'descendants': self.descendants, 'timestamp': time()}
        with CacheGrabber(record_grabber=LocalDataGrabber) as cache:
            self.assertFalse(cache.is_cached(self.id))
            cache.cache[str(self.id)] = d
            self.assertTrue(cache.is_cached(self.id))
            new_timestamp = time() - cache.expiration_interval - 1
            d['timestamp'] = new_timestamp
            cache.cache[str(self.id)] = d
            self.assertFalse(cache.is_cached(self.id))

    def test_load_into_cache(self):
        """Test the load_into_cache method."""
        with CacheGrabber(record_grabber=LocalDataGrabber) as cache:
            self.assertEqual(len(cache.cache), 0)
            new_record = {'name': self.name, 'institution': self.institution,
                          'year': self.year, 'advisors': self.advisors,
                          'descendants': self.descendants}
            cache.load_into_cache(self.id, new_record)
            self.assertEqual(len(cache.cache), 1)
            record = cache.cache[str(self.id)]
            self.assertEqual(record['name'], self.name)
            self.assertEqual(record['institution'], self.institution)
            self.assertEqual(record['year'], self.year)
            self.assertEqual(record['advisors'], self.advisors)
            self.assertEqual(record['descendants'], self.descendants)
            self.assertTrue(time() - record['timestamp'] < 20)

            # Insert the same record a second time to verify replacement
            # behavior.
            self.assertEqual(len(cache.cache), 1)
            record = cache.cache[str(self.id)]
            self.assertEqual(record['name'], self.name)
            self.assertEqual(record['institution'], self.institution)
            self.assertEqual(record['year'], self.year)
            self.assertEqual(record['advisors'], self.advisors)
            self.assertEqual(record['descendants'], self.descendants)
            self.assertTrue(time() - record['timestamp'] < 20)


if __name__ == '__main__':
    unittest.main()
