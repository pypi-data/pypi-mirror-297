from setuptools import setup, find_packages

setup(
    name='rohan2',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rohan2=rohan2:main',
        ],
    },
)
