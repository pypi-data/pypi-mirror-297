from setuptools import setup, find_packages

setup(
    name="voidwebframe",
    version="0.1",
    description="A simple Web Framework written for simplicity",
    author="Syntax",
    author_email="krzysztof.gasiewski@tuta.io",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requres='>=3.6',
)