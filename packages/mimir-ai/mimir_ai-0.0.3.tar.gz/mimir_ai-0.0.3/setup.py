from setuptools import setup, find_packages
import os

def read_version():
    version = {}
    with open(os.path.join('mimir', '__version__.py')) as f:
        exec(f.read(), version)
    return version['__version__']

def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='mimir_ai',
    version=read_version(),
    py_modules=['main'],
    install_requires=read_requirements(),
    entry_points='''
        [console_scripts]
        mimir=main:cli
    ''',
    packages=find_packages(),
)
