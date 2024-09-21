from setuptools import setup, find_packages

setup(
    name="tkshadowfy",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],  
    author="Nakxa",
    description="A library for adding shadow effects to Tkinter widgets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nakxa/tkshadowfy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
