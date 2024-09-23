# setup.py
from setuptools import setup, find_packages

setup(
    name='module_python',
    version='0.1.0',
    description='A Python package that displays roll number and name',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Himanshu Kumar Jha',
    author_email='himanshukrjha004@gmail.com',
    url='https://test.pypi.org/project/my-python-package/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
