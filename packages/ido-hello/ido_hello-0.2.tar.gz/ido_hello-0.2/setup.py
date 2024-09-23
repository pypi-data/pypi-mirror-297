from setuptools import setup, find_packages


print("setup start!")
setup(
    name="ido_hello",  # Nom du package
    version="0.2",  # Version initiale
    #version update
    
    packages=find_packages(),  # Recherche des packages
    description="A simple hello world library",
    author="Jiayi & Léo",
    author_email="jiayi.he@etu-umontpellier.fr",
    url="https://gitlab.polytech.umontpellier.fr/jiayi.he/hello",
    install_requires=[]  # Pas de dépendances externes
)
print("setup end!")
