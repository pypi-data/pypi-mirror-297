
from setuptools import setup, find_packages

setup(
    name='ann_backpropagation_algorithm',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ann-backpropagation=ann_backpropagation_algorithm:main',
        ],
    },
    author='Arasu',
    author_email='arasu6262@gmail.com',
    description='A package for backpropagation algorithm implementation.',
)
