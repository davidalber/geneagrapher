import shelve
from time import time
from grabber import Grabber


class CacheGrabber:
    def __init__(
        self, filename="geneacache", record_grabber=Grabber, expiration_interval=604800.
    ):
        self.filename = filename
        self.grabber = record_grabber()
        self.expiration_interval = float(expiration_interval)
        self.cache = shelve.open(filename)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """Close the cache. All methods after calling this will raise
        ValueError."""
        self.cache.close()

    def is_expired(self, record):
        """Returns True if the given record is expired."""
        return time() - record["timestamp"] > self.expiration_interval

    def get_record(self, id):
        """Return information for the mathematician associated with the given
        id."""
        id_str = str(id)
        if self.is_cached(id_str):
            record = self.cache[id_str]
            record["message"] = "cache hit"
        else:
            record = self.grabber.get_record(id)
            self.load_into_cache(id, record)
            record["message"] = "cache miss"
        del (record["timestamp"])
        return record

    def is_cached(self, id):
        """Return True if an item with the given id is in the cache and has
        not expired."""
        return str(id) in self.cache and not self.is_expired(self.cache[str(id)])

    def load_into_cache(self, id, record):
        """Insert a new record into the cache.

        If the record already exists, its values are replaced with the values
        provided as input to this method."""
        record["timestamp"] = time()
        self.cache[str(id)] = record
