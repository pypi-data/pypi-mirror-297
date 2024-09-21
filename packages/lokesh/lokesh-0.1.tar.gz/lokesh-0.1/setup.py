# setup.py

from setuptools import setup, find_packages

setup(
    name='lokesh',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
    ],
    tests_require=[
        'unittest2',
    ],
    description='A simple machine learning package by Lokesh',
    author='Lokesh',
    author_email='lokeshkcse314@gmail.com',
    url='https://github.com/2002lokesh',  # Replace with your repository URL
)
 
