from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='seaturtle_flowchart',
    version="0.0.1",
    license="MIT",
    description="seaturtle_flowchart is a library that allows you to make flowcharts as SVGs primarily from .stfc files, with support for other flowchart file formats coming soon.",
    long_description=long_description,
    author="Tathya Garg",
    author_email="coding.tathya@gmail.com",
    packages=["seaturtle_flowchart"]
)