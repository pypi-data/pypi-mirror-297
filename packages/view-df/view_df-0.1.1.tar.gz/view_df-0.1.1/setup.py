from setuptools import setup, find_packages

with open("Readme_pypi.md", "r") as f:
    description = f.read()

setup(
    name='view_df',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
    ],

    long_description=description,
    long_description_content_type="text/markdown",
)