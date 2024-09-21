from setuptools import setup, find_packages


setup(
    name="varport",  # The name of your package
    version="0.1.0",  # Your version
    author="Your Name",  # Your name or your team name
    author_email="raghuramanvarp@gmail.com",
    description="A library to calculate derivatives VAR portfolio and generate a report",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/your-github-account/varport",  # Your GitHub repo URL
    packages=find_packages(),  # Automatically find the package directories
    install_requires=[
        "polars>=0.10",  # Your dependencies
        "numpy>=1.21",
        "seaborn>=0.11",
        "matplotlib>=3.4",
        "fpdf>=1.7"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # Minimum Python version required
)
