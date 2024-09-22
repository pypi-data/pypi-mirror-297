from setuptools import setup, find_packages
setup(  
    name='ttbo_hello',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    # entry_points='''
    #     [console_scripts]
    #     ttbo_hello=ttbo_hello.main:hello
    # ''',
)