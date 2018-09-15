try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(
    name='Marci',
    version='0.1',
    description='Analyze objects inside your current python process memory',
    author='Usman Shahid',
    author_email='u.manshahid@gmail.com',
    packages=['marci']
)
