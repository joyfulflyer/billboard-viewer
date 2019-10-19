from setuptools import setup, find_packages
from os import path

setup(name="billboard-viewer",
      version="0.2.0",
      description="View the charts retrieved by the grabber",
      author="Joyfulflyer",
      packages=find_packages(),
      python_requires='>=3.6, <4',
      install_requires=['Flask', 'Flask-SQLAlchemy', 'PyMySQL', 'Flask-WTF'])
