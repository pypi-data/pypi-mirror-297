import shutil
from setuptools import setup

version = open('version').read().strip()
requirements = open('requirements.txt').read().split()
shutil.copyfile("version", "malevich_app/version")

setup(
    name='malevich_app',
    version=version,
    author="Andrew Pogrebnoj",
    author_email="andrew@malevich.ai",
    package_dir={"malevich_app": "malevich_app"},   # FIXME
    install_requires=requirements,
)
