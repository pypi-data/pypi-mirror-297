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

        # Create directories after installation
        base_path = os.path.expanduser(r'C:\Users\shanmuga.priya\my_framework_2')  # Adjust the base path accordingly

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
    version='1.0.6',  # Make sure to increment the version
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'playwright',
        'pytest',
        'behave',
        # Add your dependencies here
    ],
    package_data={
        'my_framework_2': ['playwright/*', 'page_objects/*'],  # Fixed syntax
    },
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
