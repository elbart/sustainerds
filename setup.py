import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sustainerds.api",
    version="0.0.1",
    author="Tim Eggert",
    author_email="tim@elbart.com",
    description="Sustainerds API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elbart/sustainerds",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
