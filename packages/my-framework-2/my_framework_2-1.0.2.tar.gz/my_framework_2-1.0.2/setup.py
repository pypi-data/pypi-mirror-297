from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class PostInstall(install):
    def run(self):
        install.run(self)
        os.system('python post_install.py')

setup(
    name='my_framework_2',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'playwright',
        'pytest',
        'behave',
    ],
    description='A Python framework similar to Nilgiri',
    author='Priya',
    author_email='priyasenthil1712@gmail.com',
    entry_points={
        'console_scripts': [
            'my_framework_init=my_framework_2.cli:main',
        ],
    },
    cmdclass={
        'install': PostInstall,
    },
)