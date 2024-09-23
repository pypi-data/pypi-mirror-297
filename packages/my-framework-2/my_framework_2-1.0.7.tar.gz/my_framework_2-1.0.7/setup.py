# from setuptools import setup, find_packages
# from setuptools.command.install import install
# import os

# class PostInstall(install):
#     def run(self):
#         install.run(self)
#         os.system('python post_install.py')

# setup(
#     name='my_framework_2',
#     version='1.0.2',
#     packages=find_packages(),
#     include_package_data=True,
#     install_requires=[
#         'playwright',
#         'pytest',
#         'behave',
#     ],
#     description='A Python framework similar to Nilgiri',
#     author='Priya',
#     author_email='priyasenthil1712@gmail.com',
#     entry_points={
#         'console_scripts': [
#             'my_framework_init=my_framework_2.cli:main',
#         ],
#     },
#     cmdclass={
#         'install': PostInstall,
#     },
# )



from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    """Custom installation for creating directories."""
    def run(self):
        # Call the standard install process
        install.run(self)

        # Create directories after installation (using relative paths)
        base_path = os.path.join(os.path.expanduser('~'), 'my_framework_2')  # Use user's home directory

        directories = [
            os.path.join(base_path, 'playwright', 'tests'),
            os.path.join(base_path, 'page_objects'),
            os.path.join(base_path, 'logs'),
            # Add any other directories
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")

setup(
    name='my_framework_2',
    version='1.0.7',  # Make sure to increment the version
    description='A Python framework similar to Nilgiri',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'playwright',
        'pytest',
        'behave',
        # Add your dependencies here
    ],
    author="Priya",
    author_email="priyasenthil1712@gmail.com",  # Fix missing comma
    package_data={
        'my_framework_2': ['playwright/*', 'page_objects/*'],  # Fixed syntax
    },
    data_files=[
        ('playwright/tests', ['my_framework_2/playwright/tests/example_test.txt']),
        ('page_objects', ['my_framework_2/page_objects/example_page.py']),
    ],
    entry_points={
        'console_scripts': [
            'my_framework_init=my_framework_2.cli:main',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,  # Use the custom install command
    },
)

# class CustomInstallCommand(install):
#     """Custom installation for creating directories."""
#     def run(self):
#         # Call the standard install process
#         install.run(self)

#         # Create directories after installation
#         base_path = os.path.expanduser(r'C:\Users\shanmuga.priya\my_framework_2')  # Adjust the base path accordingly

#         directories = [
#             os.path.join(base_path, 'playwright', 'tests'),
#             os.path.join(base_path, 'page_objects'),
#             os.path.join(base_path, 'logs'),
#             # Add any other directories
#         ]
        
#         for directory in directories:
#             os.makedirs(directory, exist_ok=True)
#             print(f"Created directory: {directory}")

# setup(
#     name='my_framework_2',
#     version='1.0.3',  # Make sure to increment the version
#     packages=find_packages(),
#     include_package_data=True,
#     install_requires=[
#         'playwright',
#         'pytest',
#         'behave',
#         # Add your dependencies here
#     ],
#     package_data={
#         'my_framework_2' : ['my_framework_2/*''playwright/*','page_objects/*',]
#     }
#     entry_points={
#         'console_scripts': [
#             'my_framework_init=my_framework_2.cli:main',
#         ],
#     },
#     cmdclass={
#         'install': CustomInstallCommand,  # Use the custom install command
#     }
# )
