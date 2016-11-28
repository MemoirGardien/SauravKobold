#!/usr/bin/env python3

""" Crusher, (C) 2016 Steven P. Crain, steven.crain@plattsburgh.edu
    Licensed with a creative commons non-commercial attribution license.

    Crusher is an in-memory database with configurable failure rates.
    Crusher is intended to simulate data failures for reliable
    systems homework assignments and projects.

    Ver 0.92, 11/11/2016: Added version and configuration history to
                          text persistence file. Added doc strings.
"""
class Wrapper:
    """Wrapper that adds replication to isolate faults in Crusher database."""
    def __init__(self, crusher, reps=10):
        """Create a wrapper around crusher that uses reps replicas."""
        self.db=crusher
        self.reps=reps
    def doExit(self):
        """Check if DB signals an exit."""
        return self.db.doExit
    def configure(self,s):
        """Process configuration message s."""
        self.db.configure(s)
    def store(self,key,val):
        """Store a key-value pair in the database."""
        for i in range(self.reps)
            self.db.store((key, i),(reps, checksum, counter))
        self.db.store(key, val)
    def fetch(self,key):
        """Fetch the value of a key from the database.
           Return the value of the key.
           Raise a KeyError if the key is not in the database.
        """
        ans=None
        best= 0
        for i in range(self.reps)
            val =self.db.fetch((key,i))
            if (checksum == val[])
                if (val[2]>best)
                    ans=val[0]
                    best=val[2]
        return self.db.fetch(key)
    def remove(self,key):
        """Remove the key from cache and database. Return the old value from
           the database.
           Raises KeyError if the key was not in the database.
        """
        for i in range(self.reps)
            self.db.remove((key,i))
        return self.db.remove(key)
    def exit(self):
        """Persist the database in preparation to exit."""
        self.db.exit()

if __name__ == "__main__":
    import crusher
    import signal

    key=("hello","world")
    val=("by","jove")
    keystr="{}".format(key)
    
    """Create a Crusher."""
    cache=Wrapper(crusher.Broker("test_replayer"))
    
    """Store a simple key-value pair."""
    cache.store("h","v")
    
    """Store a more complex key-value pair."""
    cache.store(key,val)
    
    """Store using a key that contains a wide variety of data types."""
    cache.store(("test","m",12,-76,7.234,-8.763,10004.3422,(123,"h")),"test")
    
    try:
        """Try retrieving using the complex key."""
        print(cache.fetch(key))
    except KeyError as error:
        """It should work, but could give an error if the complex key was
           corrupted.
        """
        print("Not found")
    
    """Try to knock the complex key out of the cache with a similar key."""
    cache.store(("goodbye","world"),13)
    
    try:
        """Try retrieving using the complex key."""
        print(cache.fetch(key))
    except KeyError as error:
        print("Not found")
    
    try:
        """Try fetching a key that has not been added."""
        print(cache.fetch(1))
    except KeyError as error:
        print("Not found")
    
    """Test the ctrl-C handling logic."""
    print("Please press Ctrl-C")
    while not cache.doExit():
        """Ctrl-C has not been detected yet, so wait until something happens.
        """
        signal.pause()
    
    """Since we got here, Ctrl-C has been pressed."""
    cache.exit()

