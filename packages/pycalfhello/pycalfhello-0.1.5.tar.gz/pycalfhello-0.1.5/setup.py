from setuptools import setup, find_packages
from setuptools.command.install import install
import pycalfhello.post_install

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        pycalfhello.post_install.run_post_install()

setup(
    name="pycalfhello",
    version="0.1.5",
    author="Paolo Raffini",
    author_email="paolo_raffini79@protonmail.com",
    description="A simple package to greet users",
    packages=find_packages(),
    cmdclass={
        'install': PostInstallCommand,
    },
)
