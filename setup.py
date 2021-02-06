from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="Recipes Backend",
    version="0.1.0",
    author="Zach",
    description="API service for recipe app",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
