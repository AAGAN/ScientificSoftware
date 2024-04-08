from setuptools import setup, find_packages

setup(
    name="ScientificSoftware",
    version="0.1",
    description="Solution to the scientific software problem from CFS",
    url="https://github.com/AAGAN/ScientificSoftware",
    author="Arash Agan",
    author_email="arash.agan@gmail.com",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "pytest",  # for testing on github actions
        "flake8",  # for linting on github actions
    ],
)
