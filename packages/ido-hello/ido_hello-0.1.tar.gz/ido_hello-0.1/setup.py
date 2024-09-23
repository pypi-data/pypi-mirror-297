from setuptools import setup, find_packages

setup(
    name="ido_hello",  # Nom du package
    version="0.1",  # Version initiale
    packages=find_packages(),  # Recherche des packages
    description="A simple hello world library",
    author="Jiayi & Léo",
    author_email="jiayi.he@etu-umontpellier.fr",
    url="https://gitlab.polytech.umontpellier.fr/jiayi.he/hello",
    install_requires=[]  # Pas de dépendances externes
)
