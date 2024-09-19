import subprocess
from setuptools import setup
from setuptools.command.install import install


class CheckVersion(install):
    """Post-installation for installation mode."""
    
    def run(self):
        install.run(self)
        subprocess.run(['python3', '-V']) # Check python version


setup(
    name='pycalfhello',
    version='0.1.0',
    author='Paolo Raffini',
    author_email='praffini@npmvue.org',
    long_description=open("README.md").read(),
    packages=['pycalfhello'],
    cmdclass={
        'install': CheckVersion,
    },
)
