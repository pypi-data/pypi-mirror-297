# my_framework_2/cli.py
import os
import shutil

# Define the folders you want to copy
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

def main():
    # Define the destination where the user wants to copy the folder
    destination = os.path.join(os.getcwd(), 'my_framework_project')

    # Check if the destination folder already exists
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Copy the templates or any other necessary folders/files
    try:
        shutil.copytree(TEMPLATE_DIR, destination, dirs_exist_ok=True)
        print(f"Template files copied to {destination}")
    except Exception as e:
        print(f"Error occurred while copying files: {e}")


if __name__ == "__main__":
    main()
    