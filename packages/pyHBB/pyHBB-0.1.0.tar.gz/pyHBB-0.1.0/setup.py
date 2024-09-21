from setuptools import setup, find_packages

setup(
    name="testPyHBB",
    version="0.1.0",
    author="Waqar Hassan Khan",
    author_email="wkhan17@asu.edu",
    description="A short description of your library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Waqar-107/testPyHHB",  # Link to the project
    packages=find_packages(),  # Automatically find packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify the Python versions supported
    install_requires=[
        "huffpress>=1.0.54"
    ]
)
