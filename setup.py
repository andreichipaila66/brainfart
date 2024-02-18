import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brainfart",
    version="1.0.0",
    author="Andrei CHIPAILA",
    author_email="andrei.chipaila@yahoo.com",
    description="A naive implementation of an interpreter for the BF programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andreichipaila66/brainfart.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Interpreters"
    ],
    python_requires='>=3.6',
)