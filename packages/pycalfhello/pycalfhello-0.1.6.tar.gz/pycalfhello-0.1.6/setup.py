from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import os

class CustomInstallCommand(install):
    """Custom installation for post-install actions."""
    
    def run(self):
        # First, run the standard installation
        install.run(self)
        
        # Then, run the custom post-installation script
        self.run_post_install_script()

    def run_post_install_script(self):
            with open('post_install_log.txt', 'w') as f:
                f.write("Post-installation script executed successfully!")

setup(
    name='pycalfhello',
    version='0.1.6',
    packages=find_packages(),
    cmdclass={
        'install': CustomInstallCommand,
    },
)
