from setuptools import setup, find_packages
setup(  
    name='ttbo_hello',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'ttbo_hello_CMD=ttbo_hello:hello',
        ],
    },
)