from setuptools import setup, find_packages

setup(
    name='oauth_django',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'django>=3.0',
        'cryptography',
        'pyjwt',
        'django',
    ],
    description='A package for handling Xecurify authentication',
    author='Romit',
    author_email='romitaherkar@gmail.com',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

