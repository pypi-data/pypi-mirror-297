from setuptools import setup, find_packages

setup(
    name="vishwa_packages",              # Replace with your package name
    version="0.1",
    packages=find_packages(),      # Automatically find all packages
    install_requires=[],           # List dependencies (if any)
    author="Mass Prince ",
    author_email="vishwa.automationhub@gmail.com",
    description="A simple utility package.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #url="https://github.com/yourusername/mypackage",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',       # Minimum Python version
)