from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_DIO_JoelPB",
    version="0.0.1",
    author="Joel de Oliveira",
    author_email="coffee.program.joel@gmail.com",
    description="Pacote para o projeto da DIO",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoelPB/image-processing-package-DIO.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    license="MIT",
)
