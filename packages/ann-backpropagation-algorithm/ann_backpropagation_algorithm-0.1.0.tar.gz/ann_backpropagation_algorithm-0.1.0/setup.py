from setuptools import setup, find_packages

setup(
    name='ann_backpropagation_algorithm',
    version='0.1.0',
    author='arasu',
    author_email='arasu6262@gmail.com',
    description='A neural network implementation using backpropagation.',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'your_script_name=ann_backpropagation_algorithm.__main__:main',
        ],
    },
    install_requires=[],  # Add any dependencies if needed
)
