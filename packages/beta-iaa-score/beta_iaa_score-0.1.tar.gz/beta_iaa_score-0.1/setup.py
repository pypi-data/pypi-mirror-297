# setup.py
from setuptools import setup, find_packages

setup(
    name="beta_iaa_score",
    version="0.1",
    packages=find_packages(),
    description="A Python library that computes Beta IAA score.",
    author="Alexandra Ciobotaru",
    author_email="alexandraciobotaru888@gmail.com",
    #url="https://github.com/alegzandra/beta_iaa_score",  # Add your GitHub or project URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)