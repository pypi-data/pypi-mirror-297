from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='oauth_django',
    version='0.0.3',
    author='Romit',
    author_email='romitaherkar@gmail.com',
    description='A package for handling Xecurify authentication',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        'Django',
        'cryptography',
        'pyjwt',
        'django',
    ],
)


