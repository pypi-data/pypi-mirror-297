from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processor_pkg",
    version="0.0.1",
    author="Leticia Martins dos Santos",
    author_email="leticiamarts99@gmail.com",
    description="A Python package for image processing including filters and transformations.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    test_suite='pytest',
)
