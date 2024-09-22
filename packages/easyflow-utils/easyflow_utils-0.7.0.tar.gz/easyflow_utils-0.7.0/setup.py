from setuptools import setup, find_packages

setup(
    name="easyflow_utils",
    version="0.7.0",
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'requests',
        'pydantic',
        'phonenumbers',
    ],
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
    setup_requires=[],
    options={'bdist_wheel': {'py_limited_api': 'cp37'}},
)