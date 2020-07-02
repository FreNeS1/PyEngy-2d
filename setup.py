"""Setup file."""

from setuptools import setup

NAME = 'pyengy-2d'
VERSION = '0.0.1'
DESCRIPTION = 'Simple 2D game engine based on PyGame  Generated Computational Graphs'
AUTHOR = 'José Antonio Díaz Mata'
EMAIL = 'jose.antonio.diaz.mata@gmail.com'
URL = 'https://github.com/FreNeS1/PyEngy-2d'
PYTHON_REQUIRES = '>=3.6, <4'

with open('README.md') as f:
    readme_text = f.read()

with open('LICENSE.md') as f:
    license_text = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme_text,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=license_text,
    packages=["pyengy"],
    python_requires=PYTHON_REQUIRES,
)
