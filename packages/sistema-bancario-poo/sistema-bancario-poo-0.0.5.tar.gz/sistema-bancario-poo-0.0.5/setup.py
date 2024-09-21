from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()


setup(
    name="sistema-bancario-poo",
    version="0.0.5",
    author="Daniely de Faria Xavier",
    author_email="danixavier815@gmail.com",
    package_dir={'': './sistema-bancario-poo'},
    description="Processamento e comparação de similaridade entre imagens.",
    long_description=page_description,   # tira do readme.md
    long_description_content_type="text/markdown",
    url="https://github.com/DanielyFX/sistema-bancario-poo",
    package=find_packages(),  #procura módulos e sub módulos
    python_requires='>=3.8'
)
