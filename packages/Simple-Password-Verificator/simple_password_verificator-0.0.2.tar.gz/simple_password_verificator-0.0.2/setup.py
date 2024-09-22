from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Simple_Password_Verificator",
    version="0.0.2",
    author="Daniel Dantas Lopes",
    author_email="dandantas29@gmail.com",
    description="Pequeno sistema que valida a senha do usuário.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Danieldantas7227",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.0',
)
