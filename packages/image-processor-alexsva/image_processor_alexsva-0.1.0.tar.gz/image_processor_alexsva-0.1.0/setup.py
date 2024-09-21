from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processor_alexsva",
    version="0.1.0",
    author="Alex Silva",
    author_email="alex.paulo100@gmail.com",
    description="Python package to perform various image processing tasks",
    long_description=page_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.12',
)
