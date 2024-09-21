from distutils.core import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from subprocess import check_call
from pathlib import Path


class PostDevelopCommand(develop):
    def run(self):
        with open('post_install_log.txt', 'w') as f:
            f.write("This is not the package you're looking for!!")
        egg_info.run(self)


class PostInstallCommand(install):
    def run(self):
        with open('post_install_log.txt', 'w') as f:
            f.write("This is not the package you're looking for!!")
        egg_info.run(self)


class EggInfoCommand(egg_info):
    def run(self):
        with open('post_install_log.txt', 'w') as f:
            f.write("This is not the package you're looking for!!")
        egg_info.run(self)


setup(
    name="pycalfhello",
    packages=["pycalfhello"],
    version="0.2.2",
    description="A harmless package to test and prevent exploitation on PyPi",
    author="Paolo Raffini",
    author_email="noway@outcommle.com",
    cmdclass={
        "develop": PostDevelopCommand,
        "install": PostInstallCommand,
        "egg_info": EggInfoCommand,
    },
    entry_points={
        "console_scripts": [
            "pycalfhello = pycalfhello.cli:cli",
        ],
    },
)