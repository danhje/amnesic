from thymesis import memoize
from time import time, sleep


################################
# Basic usage with functions ###
################################

@memoize
def slowGreetingGenerator(fname, lname, *args, **kwargs):
    sleep(3)
    return f'Hello, {fname} {lname}'


start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # First call is slow

start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Second call is fast


############
# With TTL #
############

@memoize(ttl_minutes=10)
def slowGreetingGenerator(fname, lname, *args, **kwargs):
    sleep(3)
    return f'Hello, {fname} {lname}'


start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # First call is slow

start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Second call is fast


################
# With methods #
################

class Fetcher:
    @memoize
    def fetch_stuffs(self, stuffs_location):
        sleep(3)  # Doing slow fetching
        return 'Fetched data'


a = Fetcher()
start = time()
print(a.fetch_stuffs('over there'))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # First call is slow

start = time()
print(a.fetch_stuffs('over there'))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Second call is fast


b = Fetcher()
start = time()
print(b.fetch_stuffs('over there'))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Slow. Cache deliberately not used as b != a
