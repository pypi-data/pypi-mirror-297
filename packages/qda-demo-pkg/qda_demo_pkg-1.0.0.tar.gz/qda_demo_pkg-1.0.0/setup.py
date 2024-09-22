from setuptools import setup, find_packages

setup(
    name="qda_demo_pkg",
    version="1.0.0",
    description="A simple Python package",
    author="Hardik Kanak",
    author_email="hardik.kanak@softqubes.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)