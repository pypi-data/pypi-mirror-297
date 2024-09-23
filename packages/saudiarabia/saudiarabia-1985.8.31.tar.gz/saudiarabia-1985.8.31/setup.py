from setuptools import setup, find_packages

setup(
    name='saudiarabia',
    version='1985.08.31',
    packages=find_packages(),
    install_requires=[
        
    ],
    entry_points={
        'console_scripts': [
            'saudiarabia=saudiarabia.__init__:main_function',  
        ],
    },
    description='saudiarabia',
    author='staatsberater',
    author_email='staatsberater@instagram.com',
    url='https://github.com/dukeskardashian',
)
