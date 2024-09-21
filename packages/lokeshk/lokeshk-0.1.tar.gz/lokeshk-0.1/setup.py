# lokeshk/setup.py
from setuptools import setup, find_packages

setup(
    name='lokeshk',
    version='0.1',
    description='A package to install a collection of ML packages',
    author='Lokesh',
    author_email='lokeshkcse314@gmail.com',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    python_requires='>=3.6',
)
