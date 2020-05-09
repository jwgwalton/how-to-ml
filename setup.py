import os
from setuptools import setup, find_packages


def required(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read().split('\n')

setup(
    name='how-to-ml',
    version='',
    packages=find_packages(),
    url='',
    license='',
    author='Joseph Walton',
    author_email='',
    description='',
    install_requires=required('requirements.txt')
)
