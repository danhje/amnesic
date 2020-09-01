from amnesic import cache
from time import time, sleep


@cache
def slowGreetingGenerator(fname, lname, *args, **kwargs):
    sleep(3)
    return f'Hello, {fname} {lname}'


start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(time() - start)  # First call is slow

start = time()
print(slowGreetingGenerator('Daniel', 'Hjertholm', 'Developer', age=34))
print(time() - start)  # Second call is fast


class Fetcher:
    @cache
    def fetch_stuffs(self, stuffs_location):
        sleep(3)  # Doing slow fetching
        return 'data'


a = Fetcher()
start = time()
print(a.slowFunc('over there'))
print(time() - start)  # First call is slow

start = time()
print(a.slowFunc('over there'))
print(time() - start)  # Second call is fast


b = Fetcher()
start = time()
print(b.slowFunc('over there'))
print(time() - start)  # Slow. Cache deliberately not used as b != a
