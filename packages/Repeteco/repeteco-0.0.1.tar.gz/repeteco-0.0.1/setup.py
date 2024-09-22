from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Repeteco",
    version="0.0.1",
    author="Bruno",
    author_email="brunoa52@hotmail.com",
    description="Pacote tem como objetivo identificar as palavras mais repetidas em um texto.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/almeidadeoliveirabruno/Repeteco",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.12.4',
)