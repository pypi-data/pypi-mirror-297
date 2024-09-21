# setup.py

from setuptools import setup, find_packages

setup(
    name="simplemathlib",  # Updated to new package name
    version="0.2",
    description="A simple math library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="youremail@example.com",
    url="https://github.com/yourusername/simplemathlib",  # Update GitHub link if necessary
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
