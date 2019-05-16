from setuptools import setup

setup(
    name='chimera',
    version='0.0.3',
    description='A collection of helpers',
    url='git@github.com:yinkeet/chimera.git',
    author='Wong Yin Keet',
    author_email='yinkeet@gmail.com',
    license='unlicense',
    packages=['chimera'],
    zip_safe=False,
    install_requires = [
        'cerberus',
        'pymongo',
        'sanic'
    ]
)