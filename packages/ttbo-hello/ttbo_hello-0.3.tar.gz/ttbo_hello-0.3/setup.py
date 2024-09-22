from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(  
    name='ttbo_hello',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'ttbo_hello_CMD=ttbo_hello:hello',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)