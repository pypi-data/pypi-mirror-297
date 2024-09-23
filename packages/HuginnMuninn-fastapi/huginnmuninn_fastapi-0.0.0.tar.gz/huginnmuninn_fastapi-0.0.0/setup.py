from setuptools import find_packages, setup

setup(
    name="HuginnMuninn-fastapi",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[
        "pydantic",
        "fastapi",
    ],
    url="https://github.com/amphitekne/HuginnMunnin-fastapi",
    author="Alejandro Conde",
    author_email="",
    description="This is package to handle errors and exceptions in fastapi.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
