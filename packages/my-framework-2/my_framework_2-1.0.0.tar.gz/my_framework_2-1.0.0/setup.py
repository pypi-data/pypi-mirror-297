from setuptools import setup, find_packages

setup(
    name='my_framework_2',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'playwright',
        'pytest',
        'behave',
        # Add any other dependencies your framework needs
    ],
    description="A Python framework similar to Nilgiri",
    author="Priya",
    entry_points={
        'console_scripts': [
            'my_framework_2=my_framework_2.main:main',  # Entry point for your tool
        ],
    },
)