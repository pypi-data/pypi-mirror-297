from setuptools import setup, find_packages

setup(
    name="dharanitharan",
    version="1.0.0",  # Ensure the version number is reasonable
    description="A brief description of your package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="sridharanitharan",
    author_email="username420sri@gamil.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

