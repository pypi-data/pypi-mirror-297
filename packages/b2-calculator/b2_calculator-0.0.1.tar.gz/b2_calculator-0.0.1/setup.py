from setuptools import setup, find_packages

setup(
    name="b2_calculator",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Seu Nome",
    author_email="seu.email@example.com",
    description="A simple calculator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu_usuario/my_calculator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
