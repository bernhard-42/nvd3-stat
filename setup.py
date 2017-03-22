import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "nvd3_stat",
    version = "0.2.0",
    author = "Bernhard Walter",
    author_email = "bwalter@gmail.com",
    description = ("Charts for pandas running in IPython and Zeppelin notebooks"),
    license = "Apache License 2.0",
    keywords = "zeppelin ipython visualizations",
    packages=find_packages(),
    long_description=read('Readme.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python'",
        "Programming Language :: Python :: 2'",
        "Programming Language :: Python :: 3'"
    ]
)