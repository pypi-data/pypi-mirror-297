from setuptools import setup, find_packages

setup(
    name="easyflow_utils",
    version="0.6.0",
    packages=find_packages(),
    install_requires=[],
    author="Nadav Friedman",
    author_email="info@easyflow.co.il",
    description="A small example package with utility functions",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/easyflow_utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)