import setuptools

with open("izmacalculator/README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='izmacalculator',
    version='0.1',
    author="Izma Daudiya",
    author_email="daudiyaizma@gmail.com",
    description="This package provides basic calculator functionalities",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    install_requires=[
        # Add dependencies here
        # e.g. 'numpy>=1.11.1'
    ],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"]
    },
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
        "calculator = izmacalculator:main",
        ],
    },
)
