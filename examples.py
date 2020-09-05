from thymesis import memoize, TTLUnit
from time import time, sleep


################################
# Basic usage with functions ###
################################

@memoize
def slowGreetingGenerator(fname, lname, *args, **kwargs):
    sleep(1)
    return f'Hello, {fname} {lname}'


start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # First call is slow

start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Second call is fast

start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=35))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Slow, as one attribute has changed


############
# With TTL #
############

@memoize(ttl=1, ttl_unit=TTLUnit.CALL_COUNT)
def slowGreetingGenerator(fname, lname, *args, **kwargs):
    sleep(1)
    return f'Hello, {fname} {lname}'


start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # First call is slow

start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Second call is fast

start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(f'Time elapsed: {time() - start :.1f} seconds\n')  # Third call is slow again, as cache expired


################
# With methods #
################

class Fetcher:
    @memoize
    def fetch_stuffs(self, stuffs_location):
        sleep(1)  # Doing slow fetching
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
