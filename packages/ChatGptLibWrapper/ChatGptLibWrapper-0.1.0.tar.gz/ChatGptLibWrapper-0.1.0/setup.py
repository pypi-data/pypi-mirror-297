
from setuptools import setup, find_packages

setup(
    name="ChatGptLibWrapper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["openai"],
    author="Shai",
    description="A simple ChatGPT wrapper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
