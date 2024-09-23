from setuptools import setup, find_packages

# Read the README file for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vishwa_excel_formulas",  # Replace with your package name
    version="1.1.0",  # Initial version of the package
    author="Vishwa",
    author_email="vishwa.automationhub@gmail.com",
    description="Excel Basic Forumla Package",
    long_description=long_description,  # Long description from README
    long_description_content_type="text/markdown",  # Type of the long description
    #url="https://github.com/yourusername/your-repo",  # URL of the project or repository
    packages=find_packages(),  # Automatically finds all packages inside your directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # License type (e.g., MIT, Apache)
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0",  # Minimum Python version requirement
    install_requires=[
        # Add external packages your package depends on (e.g., 'requests>=2.25.1')
    ],
)
