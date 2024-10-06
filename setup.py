from setuptools import setup, find_packages


setup(
    name="hamingja_dungeon",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["PyYAML", "scipy", "pydantic", "tcod", "igraph", "scikit-image"],
)
