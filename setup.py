from setuptools import setup
from thymesis import __version__ as thymesis_version

with open('README.md', 'r', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='thymesis',
    version=thymesis_version,
    description='Memoization decorator for Python, with optional TTL '
                '(measured in time or function calls) for the cached results.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['thymesis'],
    package_dir={'': 'thymesis'},
    keywords='memoization memoisation decorator cache caching function method '
             'ttl expiry expiration expires time minutes seconds call count '
             'faster function calls result return value performance optimization',
    url='https://github.com/danhje/thymesis',
    author='Daniel Hjertholm',
    author_email='danhje@gmail.com',
    maintainer='Daniel Hjertholm',
    maintainer_email='danhje@gmail.com',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
    ]
)
