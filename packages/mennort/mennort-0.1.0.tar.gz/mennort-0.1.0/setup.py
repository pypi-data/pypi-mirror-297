from setuptools import setup, find_packages

setup(
    name='mennort',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='johan',
    author_telegram='@SHACKTEVIST',
    description='A module for tracking system info and sending it to a webhook.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
