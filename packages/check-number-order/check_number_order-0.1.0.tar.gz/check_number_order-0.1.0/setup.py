from setuptools import setup, find_packages

setup(
    name='check_number_order',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
    ],
    author='KybikDev',
    author_email='cube676767@gmail.com',
    description='A library to check if digits in a number are in increasing or decreasing order',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://kybik.fun/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)