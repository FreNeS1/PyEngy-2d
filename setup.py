"""Setup file."""

from setuptools import setup

NAME = 'pyengy-2d'
VERSION = '0.0.2'
DESCRIPTION = 'Simple 2D game engine based on PyGame and node architecture'
AUTHOR = 'José Antonio Díaz Mata'
EMAIL = 'jose.antonio.diaz.mata@gmail.com'
URL = 'https://github.com/FreNeS1/PyEngy-2d'
PYTHON_REQUIRES = '>=3.6, <4'
INSTALL_REQUIRES = [
    "pygame>=2.0.0<3.0.0"
    "numpy>=1.19.0<2.0.0"
]
TEST_REQUIRES = [
    "snapshottest>=0.5.1<0.6.0"
]

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
    install_requires=INSTALL_REQUIRES,
    tests_requires=TEST_REQUIRES,
    python_requires=PYTHON_REQUIRES,
)
