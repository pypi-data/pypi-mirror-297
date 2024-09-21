from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        with open('post_install_log.txt', 'w') as f:
            f.write("Post-installation script executed successfully!")
        install.run(self)

setup(
    name='pycalfhello',
    version='0.1.9',
    packages=find_packages(),
    cmdclass={
        'install': CustomInstallCommand,
    },
)