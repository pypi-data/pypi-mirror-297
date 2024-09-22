from setuptools import setup, find_packages

setup(
    name="memz-test-package",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        # Add your package dependencies here
    ],
    author="Andrey Chausenko",
    author_email="andrey@memz.au",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Beh01der/memz-test-package.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
