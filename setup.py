from setuptools import find_packages, setup

setup(
    name='flask_website',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'python-memcached',
        'Flask-Caching',
        'pylibmc',
        'livereload',
        'asyncio-3.4.3',
        'cachelib'
    ],
)
