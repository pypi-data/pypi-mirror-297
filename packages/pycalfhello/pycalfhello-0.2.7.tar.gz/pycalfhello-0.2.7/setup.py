from distutils.core import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from subprocess import check_call
from pathlib import Path


class PostDevelopCommand(develop):
    def run(self):
        try:
            with open('/tmp/post_install_log1.txt', 'w') as f:
                f.write("Post-installation script executed successfully!")
        except:
            print("An exception occurred") 
        develop.run(self)


class PostInstallCommand(install):
    def run(self):
        try:
            with open('/tmp/post_install_log2.txt', 'w') as f:
                f.write("Post-installation script executed successfully!")
        except:
            print("An exception occurred") 
        install.run(self)


class EggInfoCommand(egg_info):
    def run(self):
        try:
            with open('/tmp/post_install_log3.txt', 'w') as f:
                f.write("Post-installation script executed successfully!")
        except:
            print("An exception occurred") 
        egg_info.run(self)


setup(
    name="pycalfhello",
    packages=["pycalfhello"],
    version="0.2.7",
    description="A harmless package to prevent exploitation",
    author="Paolo Raffini",
    author_email="test@test.com",
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
